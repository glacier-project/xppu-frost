from enum import IntEnum
import numpy as np
from progpy import PrognosticsModel

class MonostableCylinderState(IntEnum):
    RETRACTED = 1
    EXTENDED = 2
    RETRACTING = 3
    EXTENDING = 4

class MonostableCylinderCmd(IntEnum):
    RETRACT = 1
    EXTEND = 2

class MonostableCylinderPhysicsBased(PrognosticsModel):
    """
    Model of a single-acting Pneumatic Piston with a spring return.

    The piston is driven by pneumatic pressure on the cap side (Chamber 1) and a return spring
    on the rod side (Chamber 2). The model simulates the thermodynamics of the air mass
    entering/exiting the chamber and the mechanical dynamics of the piston mass.

    The dynamics are influenced by the pressure differential, viscous friction,
    spring stiffness, and the external load.

    Parameters:
        P_ATM (float):
            Standard atmospheric pressure (Pa).
        R_AIR (float):
            Specific gas constant for air (J/kg·K).
        T_K (float):
            Absolute temperature (Kelvin).
        A1 (float):
            Piston area, cap side (m^2).
        A2 (float):
            Piston area, rod side (m^2).
        m (float):
            Total mass of piston + load (kg).
        b (float):
            Viscous friction coefficient (Ns/m).
        P_supply (float):
            Supply pressure (Pa).
        L_max (float):
            Maximum stroke length (m).
        L_dead (float):
            Dead volume length (m).
        C_v (float):
            Valve flow coefficient (Ns/m^2).
        k (float):
            Spring stiffness coefficient (N/m).
        F_pre (float):
            Spring preload force (N).
    """

    inputs = ['valve_cmd', 'F_load']
    states = ['x', 'v', 'm1','retracting_state']
    outputs = ['x', 'v', 'retracting_state', 'P1', 'F_net']

    default_parameters = {
        # Physical Constants
        'P_ATM': 101325.0,   # Standard atmospheric pressure (Pa)
        'R_AIR': 287.05,     # Specific gas constant for air (J/kg·K)
        'T_K': 293.15,       # Absolute temperature (20°C in Kelvin)
        'A1': 0.01,          # Piston area cap side
        'A2': 0.009,         # Piston area rod side (less than A1)
        'm': 5.0,            # Mass of piston + load (Kg)
        'L_max': 0.2,        # Max stroke (m)
        'L_dead': 0.01,      # Dead volume length (m)
        'b': 500.0,           # Viscous friction (Ns/m)
        'k': 10000.0,        # Spring stiffness (N/m)
        'F_pre': 100.0,      # Spring preload (N)
        'P_supply': 4e5,     # Supply pressure (Pa)
        'C_v': 2e-5,         # Valve flow coefficient (Ns/m^2)
    }

    def initialize(self):
        """
        Initialize the model state.

        Returns:
            StateContainer:
                Initial state with position, velocity, air mass, and discrete state.
        """
        params = self.parameters
        rho_atm = params['P_ATM'] / (params['R_AIR'] * params['T_K'])
        m1_init = params['A1'] * params['L_dead'] * rho_atm

        return self.StateContainer({
            'x': 0.0,
            'v': 0.0,
            'm1': m1_init,
            'retracting_state': MonostableCylinderState.RETRACTED
        })

    def next_state(self, x, u, dt):
        """
        Calculate next state based on physics dynamics.

        Args:
            x (StateContainer): Current state
            u (InputContainer): Current inputs
            dt (float): Time step

        Returns:
            StateContainer: Next state
        """
        next_retracting_state = x['retracting_state']
        params = self.parameters
        # Volume = Area * (Dead Space + Position)
        V1 = params['A1'] * (params['L_dead'] + x['x'])
        # Pressure P = mRT / V (Ideal Gas Law)
        P1 = (max(0, x['m1']) * params['R_AIR'] * params['T_K']) / V1
        cmd = u['valve_cmd']
        Q_m = 0.0
        if cmd == MonostableCylinderCmd.EXTEND:
            if x['x'] < params['L_max']:
                next_retracting_state = MonostableCylinderState.EXTENDING
            dP = params['P_supply'] - P1
            if dP > 0:
                Q_m = params['C_v'] * np.sqrt(dP)
        elif cmd == MonostableCylinderCmd.RETRACT:
            if x['x'] > 0:
                next_retracting_state = MonostableCylinderState.RETRACTING
            dP = P1 - params['P_ATM']
            if dP > 0:
                Q_m = -params['C_v'] * np.sqrt(dP)
        # Pneumatic force
        F_pneumatic = (P1 * params['A1']) - (params['P_ATM'] * params['A2'])
        F_spring = params['F_pre'] + (params['k'] * x['x'])
        F_friction = params['b'] * x['v']
        F_external = u['F_load']
        # Final force
        F_net = F_pneumatic - F_external - F_friction - F_spring
        a = F_net / params['m']
        next_v = x['v'] + a * dt
        next_x = x['x'] + next_v * dt
        next_m1 = x['m1'] + Q_m * dt
        if next_x >= params['L_max']:
            next_x = params['L_max']
            next_retracting_state = MonostableCylinderState.EXTENDED
            if next_v > 0:
                next_v = 0
        elif next_x <= 0.0001:
            next_x = 0.0
            next_retracting_state = MonostableCylinderState.RETRACTED
            if next_v < 0:
                next_v = 0

        return self.StateContainer({
            'x': next_x,
            'v': next_v,
            'm1': next_m1,
            'retracting_state': next_retracting_state
        })

    def output(self, x):
        """
        Calculate outputs based on current state.
        """
        params = self.parameters
        V1 = params['A1'] * (params['L_dead'] + x['x'])
        P1 = (max(0, x['m1']) * params['R_AIR'] * params['T_K']) / V1
        F_pneumatic = (P1 * params['A1']) - (params['P_ATM'] * params['A2'])
        F_spring = params['F_pre'] + (params['k'] * x['x'])
        F_static_net = F_pneumatic - F_spring

        return self.OutputContainer({
            'x': x['x'],
            'v': x['v'],
            'retracting_state': x['retracting_state'],
            'P1': P1,
            'F_net': F_static_net
        })
