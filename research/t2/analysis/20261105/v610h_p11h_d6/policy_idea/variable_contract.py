"""Policy vocabulary only: no plan selection, controller, or signal hardware I/O.

Future feasible set depends on verified road, movement, sensor, and legal inputs.
"""
from dataclasses import dataclass,asdict
from typing import Literal

@dataclass(frozen=True)
class FutureDecisionVariables:
    phase_green_s: tuple[str,...] = ('g_phase_1', 'g_phase_2')
    cycle_s: str='C_j'
    offset_s: str='phi_j'
    phase_order: str='pi_j'
    pedestrian_clearance_s: str='t_ped_clearance'
    yellow_s: str='t_yellow'
    all_red_s: str='t_all_red'
    min_green_s: str='g_min'
    max_green_s: str='g_max'
    priority_classes: tuple[str,...]=('bus','emergency','pedestrian')
    demand_uncertainty: str='Theta_demand'
    geometry_uncertainty: str='Theta_geometry'
    model_numeric_error: str='epsilon_numeric'
    spillback_capacity: str='K_link'
    movement_conflict_graph: str='G_conflict'
    detector_observability: str='O_sensor'
    route_legal_status: str='L_mode_time'
    objective_delay: str='J_delay'
    objective_queue: str='J_queue'
    objective_pedestrian: str='J_ped'
    objective_emissions: str='J_emissions'

    def report(self):return {'idea_only':True,'simulation_or_controller_run':False,'variables':asdict(self)}
