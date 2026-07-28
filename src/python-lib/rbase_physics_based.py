from enum import Enum
from progpy.models.dcmotor_singlephase import DCMotorSP
from progpy import PrognosticsModel
from progpy import CompositeModel
from typing import override
import math
import numpy as np

class CraneCmd(str, Enum):
    ROTATE_S = "ROTATE_S",
    ROTATE_LSC = "ROTATE_LSC",
    ROTATE_ST = "ROTATE_ST",
    PICKUP_WP = "PICKUP_WP",
    PUTDOWN_WP = "PUTDOWN_WP"

# TODO: Add NONE position
class CranePos(str, Enum):
    POS_S = "POS_S"
    POS_LSC = "POS_LSC"
    POS_ST = "POS_ST"

def update_J(params):
    # J = J_s + J_arm + J_load
    # Js, The inertia of the spinning metal shaft inside the motor itself
    # J_arm = 1/3 * m_crane * L_arm^2, The inertia of the steel arm
    # J_load = M_load * r^2, The inertia added by the object hanging from the hook
    j_load = params["mass_load"] * (params["radius_load"] ** 2)
    j_arm = (1/3) * params["m_crane"] * (params["L_arm"] ** 2)
    return {"J": params["Js"] + j_arm + j_load}


class MotorPhysicsBased(DCMotorSP):
    """Model of a rotational crane using a DC motor to rotate an arm with a load attached.
    The crane's arm rotates around a pivot point, lifting and lowering a load at a specified radius.

    The model extends the single-phase DC motor model by adding the angular position (theta) of the crane arm as a state and output variable. The crane's dynamics are influenced by the motor's troque, the load's inertia, and the arm's mass distribution.

    The total inertia (J) of the system is calculated based on the motor's shaft inertia (Js), the inertia of the crane arm (J_arm), and the inertia contributed by the load at a distance from the pivot (J_load).

    Attributes:
        process_noise (Optional[Union[float, dict[str, float]]]): Process noise applied at dx/next_state. Can be a number applied to every state, a dictionary of values for each state, or a function.
        process_noise_dist (Optional[str]): Distribution for process noise (e.g., normal, uniform, triangular)
        measurement_noise (Optional[Union[float, dict[str, float]]]): Measurement noise applied to the outputs. Can be a number applied to every output, a dictionary of values for each output, or a function.
        measurement_noise_dist (Optional[str]): Distribution for measurement noise (e.g., normal, uniform, triangular)
        L (float): Self-inductance (H)
        M (float): Mutual inductance (H)
        R (float): Armature Resistance (Ohm)
        Kt (float): back emf constant / Torque constant (V/rad/sec)
        B (float): Friction in motor / Damping (Not a function of thrust) (Nm/(rad/s))
        Js (float): Moment of inertia of motor shaft (kg*m^2)
        mass_load (float): Weight of the load (Kg)
        radius_load (float): Distance from the center of the load (Meters)
        m_crane (float): Weight of the empty arm (Kg)
        L_arm (float): Length of the arm (Meters)
        x0 (dict[str, float]): Initial state
    """

    states = DCMotorSP.states + ["theta"]
    inputs = DCMotorSP.inputs
    outputs = DCMotorSP.outputs + ["theta"]

    param_callbacks = DCMotorSP.param_callbacks | {
        "Js": [update_J],
        "mass_load": [update_J],
        "radius_load": [update_J],
        "m_crane": [update_J],
        "L_arm": [update_J]
    }

    default_parameters = DCMotorSP.default_parameters | {
        "mass_load": 0, # Weight of the load (Kg)
        "radius_load": 0.15, # Distance from the center of the load (Meters)
        "m_crane": 0, # Weight of the empty arm
        "L_arm": 0.15, # Length of the arm (Meters)
        "x0": DCMotorSP.default_parameters["x0"] | {"theta": 0.0},
    }

    def _dx(self, x, u):
        next_state = super().dx(x, u)
        dtheta_dt = x["v_rot"]  # Angular velocity is the derivative of theta

        return self.StateContainer(
            np.array(
                [*next_state.values(),
                 dtheta_dt
                ]
            )
        )

    @override
    def next_state(self, x, u, dt: float):
        dx = self._dx(x, u)
        next_state = self.StateContainer(
            {
                key: x[key] + dx[key] * dt for key in dx.keys()
            }
        )

        # Clamp theta between 0 and 2pi
        next_state["theta"] = next_state["theta"] % (2 * math.pi)
        return next_state

    def output(self, x):
        output = super().output(x)

        return self.OutputContainer(
            np.array(
                [*output.values(),
                 x["theta"]
                ]
            )
        )


class PIDController(PrognosticsModel):
    """
    Model of a general PID Controller.

    The controller receives a target setpoint and the current measurement,
    and outputs a control signal (u).

    Attributes:
        Kp (float): Proportional gain.
        Ki (float): Integral gain.
        Kd (float): Derivative gain.
        u_max (float): Maximum value of the control signal (e.g., voltage).
        u_min (float): Minimum value of the control signal (e.g., voltage).
        x0 (dict[str, float]): Initial state.
    """

    states = ["error", "integral_error", "u"]
    inputs = ["target_setpoint", "target_measurement"]
    outputs = ["u"]

    default_parameters = {
        "Kp": 5.0,
        "Ki": 2.0,
        "Kd": 0.5,
        "u_max": 12.0,
        "u_min": -12.0,
        "x0": {
            "error": 0.0,
            "integral_error": 0.0,
            "u": 0.0
        }
    }

    def output(self, x):
        """
        Returns the output control signal.

        Args:
            x (StateContainer):
                Current state containing control signal.

        Returns:
            OutputContainer:
                Output control signal (u).
        """
        return self.OutputContainer(
            np.array([x["u"]])
        )

    def next_state(self, x, u, dt):
        """
        Calculate next state with PID control logic.

        Args:
            x (StateContainer):
                Current state containing error, integral error, and control signal.
            u (InputContainer):
                Current inputs containing target_setpoint and target_measurement.
            dt (float):
                Time step.

        Returns:
            StateContainer:
                Next state with updated integral error and computed control signal.
        """
        error = u["target_setpoint"] - u["target_measurement"]
        error = (error + math.pi) % (2 * math.pi) - math.pi

        integral_error = x["integral_error"] + error * dt
        max_integral = self.parameters["u_max"] / (self.parameters["Ki"] if self.parameters["Ki"] > 0 else 1.0)
        integral_error = np.clip(integral_error, -max_integral, max_integral)

        P = self.parameters["Kp"] * error
        I = self.parameters["Ki"] * integral_error
        D = self.parameters["Kd"] * (error - x["error"])/dt

        u_command = P + I + D
        u_clamped = np.clip(
            u_command,
            self.parameters["u_min"],
            self.parameters["u_max"]
        )

        return self.StateContainer({
            "error": error,
            "integral_error": I,
            "u": u_clamped
        })

def calculate_voltage_for_target_velocity(motor_params, target_velocity, load_torque=0.0):
    """
    Calculate the voltage required to maintain a steady angular velocity.

    Args:
        motor_params (dict):
            Motor parameters including R, Kt, and B.
        target_velocity (float):
            Desired angular velocity in rad/s.
        load_torque (float):
            External load torque in N·m.

    Returns:
        float:
            Required voltage in V.
    """
    R = motor_params['R']
    Kt = motor_params['Kt']
    B = motor_params['B']
    torque_required = (B * target_velocity) + load_torque
    current_required = torque_required / Kt
    voltage_required = (current_required * R) + (Kt * target_velocity)
    return voltage_required

class RBasePhysicsBased:
    """
    Physics-based model of a rotational crane base using a DC motor and PID control.

    Args:
        motor_mass (float):
            Weight of the load attached to the crane (Kg).
        radius_load (float):
            Distance from the pivot to the load center (m).
        m_crane (float):
            Weight of the crane arm (Kg).
        L_arm (float):
            Length of the arm (m).
        Kp (float):
            Proportional gain for PID controller.
        Ki (float):
            Integral gain for PID controller.
        Kd (float):
            Derivative gain for PID controller.
        max_velocity (float):
            Maximum angular velocity (rad/s).
        target_angles (list):
            List of tuples (start_time, end_time, angle) for target setpoints.
    """

    def __init__(
        self,
        motor_mass=0.400,
        radius_load=0.10,
        m_crane=0.400,
        L_arm=0.15,
        Kp=15.0,
        Ki=1.0,
        Kd=5.0,
        max_velocity=0.698132,
        target_angles=None
    ):
        self.max_velocity = max_velocity

        # Create crane motor model
        self.crane = MotorPhysicsBased()
        self.crane.parameters["mass_load"] = motor_mass
        self.crane.parameters["radius_load"] = radius_load
        self.crane.parameters["m_crane"] = m_crane
        self.crane.parameters["L_arm"] = L_arm

        # Calculate max voltage for target velocity
        self.max_voltage = calculate_voltage_for_target_velocity(
            self.crane.parameters, max_velocity
        )

        # Create PID controller
        self.pid_controller = PIDController()
        self.pid_controller.parameters["Kp"] = Kp
        self.pid_controller.parameters["Ki"] = Ki
        self.pid_controller.parameters["Kd"] = Kd
        self.pid_controller.parameters["u_max"] = self.max_voltage
        self.pid_controller.parameters["u_min"] = -self.max_voltage

        # Create composite progpy model with connections
        connections = [
            ("PIDController.u", "MotorPhysicsBased.v"),
            ("MotorPhysicsBased.theta", "PIDController.target_measurement")
        ]

        self.composite_model = CompositeModel(
            [self.pid_controller, self.crane],
            connections=connections
        )

        # Step-by-step simulation state
        self.motor_state = None
        self.pid_state = None
        self.target_angle = 0.0
        self.is_initialized = False

    def initialize(self, initial_theta=0.0):
        """
        Initialize motor and PID states for step-by-step simulation.

        Args:
            initial_theta (float):
                Initial angle in radians.

        Returns:
            dict:
                Initial outputs with theta, v_rot, and control_voltage.
        """
        self.crane.parameters["x0"]["theta"] = initial_theta
        self.motor_state = self.crane.initialize()
        self.pid_state = self.pid_controller.initialize()
        self.target_angle = initial_theta
        self.is_initialized = True

        motor_output = self.crane.output(self.motor_state)
        pid_output = self.pid_controller.output(self.pid_state)

        return {
            "theta": float(motor_output["theta"]),
            "v_rot": float(motor_output["v_rot"]),
            "control_voltage": float(pid_output["u"])
        }

    def set_target(self, angle):
        """
        Set the target angle for the PID controller.

        Args:
            angle (float):
                Target angle in radians.
        """
        self.target_angle = angle

    def step(self, dt):
        """
        Execute one simulation step.

        Args:
            dt (float):
                Time step in seconds.

        Returns:
            dict:
                Current outputs with theta, v_rot, and control_voltage.
        """
        if not self.is_initialized:
            raise RuntimeError("RBasePhysicsBased not initialized. Call initialize() first.")

        # Get current motor angle for PID feedback
        motor_output = self.crane.output(self.motor_state)
        current_angle = float(motor_output["theta"])

        # Run PID controller step
        pid_inputs = self.pid_controller.InputContainer({
            "target_setpoint": self.target_angle,
            "target_measurement": current_angle
        })
        self.pid_state = self.pid_controller.next_state(
            self.pid_state,
            pid_inputs,
            dt
        )
        pid_output = self.pid_controller.output(self.pid_state)
        voltage = float(pid_output["u"])

        # Run motor physics step with PID output voltage
        motor_inputs = self.crane.InputContainer({
            "v": voltage,
            "t_l": 0.0
        })
        self.motor_state = self.crane.next_state(
            self.motor_state,
            motor_inputs,
            dt
        )

        # Get updated motor outputs
        motor_output = self.crane.output(self.motor_state)

        return {
            "theta": float(motor_output["theta"]),
            "v_rot": float(motor_output["v_rot"]),
            "control_voltage": voltage
        }

    def get_angle(self):
        """
        Get the current angle.

        Returns:
            float:
                Current angle in radians.
        """
        if not self.is_initialized:
            return 0.0
        motor_output = self.crane.output(self.motor_state)
        return float(motor_output["theta"])

    def get_velocity(self):
        """
        Get the current angular velocity.

        Returns:
            float:
                Current angular velocity in rad/s.
        """
        if not self.is_initialized:
            return 0.0
        motor_output = self.crane.output(self.motor_state)
        return float(motor_output["v_rot"])

    def get_control_voltage(self):
        """
        Get the current control voltage.

        Returns:
            float:
                Current control voltage in V.
        """
        if not self.is_initialized:
            return 0.0
        pid_output = self.pid_controller.output(self.pid_state)
        return float(pid_output["u"])

    def future_loading(self, t, x=None):
        """
        Define the target angle based on time.

        Args:
            t (float):
                Current time.
            x (StateContainer):
                Current state (optional).

        Returns:
            InputContainer:
                Inputs with theta_target and t_l.
        """
        theta_target = 0.0
        for start_time, end_time, angle in self.target_angles:
            if start_time <= t < end_time:
                theta_target = angle
                break
        else:
            theta_target = self.target_angles[-1][2]

        return self.composite_model.InputContainer({
            "PIDController.target_setpoint": theta_target,
            "MotorPhysicsBased.t_l": 0.0
        })
