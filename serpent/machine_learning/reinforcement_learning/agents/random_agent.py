from serpent.machine_learning.reinforcement_learning.agent import Agent

from serpent.enums import InputControlTypes

from serpent.logger import Loggers
import enum
import secrets


class RandomAgentModes(enum.Enum):
    OBSERVE = 0


class RandomAgent(Agent):

    def __init__(
        self, 
        name, 
        game_inputs=None, 
        callbacks=None, 
        seed=None,
        logger=Loggers.NOOP,
        logger_kwargs=None
    ):
        super().__init__(
            name, 
            game_inputs=game_inputs, 
            callbacks=callbacks, 
            seed=seed,
            logger=logger,
            logger_kwargs=logger_kwargs
        )

        self.mode = RandomAgentModes.OBSERVE

        self.logger.log_hyperparams(
            {"seed": seed}
        )

    def generate_actions(self, state, **kwargs):
        actions = list()

        for game_inputs_item in self.game_inputs:
            if game_inputs_item["control_type"] == InputControlTypes.DISCRETE:
                label = secrets.choice(list(game_inputs_item["inputs"].keys()))
                action = game_inputs_item["inputs"][label]

                actions.append((label, action, None))
            elif game_inputs_item["control_type"] == InputControlTypes.CONTINUOUS:
                label = game_inputs_item["name"]
                action = game_inputs_item["inputs"]["events"]

                size = 1

                if "size" in game_inputs_item["inputs"]:
                    size = game_inputs_item["inputs"]["size"]

                if size == 1:
                    input_value = secrets.SystemRandom().uniform(game_inputs_item["inputs"]["minimum"],
                        game_inputs_item["inputs"]["maximum"]
                    )
                else:
                    input_value = list()

                    for i in range(size):
                        input_value.append(
                            secrets.SystemRandom().uniform(game_inputs_item["inputs"]["minimum"],
                                game_inputs_item["inputs"]["maximum"]
                            )
                        )

                actions.append((label, action, input_value))

        for action in actions:
            self.analytics_client.track(
                event_key="AGENT_ACTION",
                data={
                    "label": action[0],
                    "action": [str(a) for a in action[1]],
                    "input_value": action[2]
                }
            )

        return actions
