import unittest
import gym
import numpy as np
import tensorflow as tf

from tf2rl.algos.vpg import VPG
from tests.algos.common import CommonAlgos, CommonDiscreteOutputAlgos, CommonContinuousOutputAlgos


class CommonActorCritic(CommonAlgos):
    def test_train(self):
        if self.agent is None:
            return
        rewards = np.zeros(shape=(self.batch_size,1), dtype=np.float32)
        dones = np.zeros(shape=(self.batch_size,1), dtype=np.float32)
        obses = np.zeros(
            shape=(self.batch_size,)+self.continuous_env.observation_space.shape,
            dtype=np.float32)
        acts = np.zeros(
            shape=(self.batch_size,self.continuous_env.action_space.low.size,),
            dtype=np.float32)
        self.agent.train_actor(
            obses, acts, obses, rewards, dones)
        self.agent.train_critic(
            obses, acts, obses, rewards, dones)


class TestContinuousVPG(CommonDiscreteOutputAlgos, CommonActorCritic):
    @classmethod
    def setUpClass(cls):
        cls.agent = VPG(
            state_shape=cls.continuous_env.observation_space.shape,
            action_dim=cls.continuous_env.action_space.low.size,
            is_discrete=False,
            gpu=-1)

    def test_get_action(self):
        if self.agent is None:
            return
        # Single input
        state = self.continuous_env.reset()
        action, log_pi = self.agent.get_action(state, test=False)
        self.assertEqual(
            action.shape[0],
            self.continuous_env.action_space.low.size)
        action, log_pi = self.agent.get_action(state, test=True)
        self.assertEqual(
            action.shape[0],
            self.continuous_env.action_space.low.size)

        # Multiple inputs
        states = np.zeros(shape=(self.batch_size, state.shape[0]))
        actions, log_pis = self.agent.get_action(states, test=False)
        self.assertEqual(
            actions.shape[0],
            self.batch_size)
        self.assertEqual(
            actions.shape[1],
            self.continuous_env.action_space.low.size)
        actions, log_pis = self.agent.get_action(states, test=True)
        self.assertEqual(
            actions.shape[0],
            self.batch_size)
        self.assertEqual(
            actions.shape[1],
            self.continuous_env.action_space.low.size)

    def test_train(self):
        # TODO: Search how to call only `CommonActorCritic`
        pass
        # super(self, CommonActorCritic).train()


# class TestDiscreteVPG(CommonDiscreteOutputAlgos):
#     @classmethod
#     def setUpClass(cls):
#         cls.agent = VPG(
#             state_shape=cls.discrete_env.observation_space.shape,
#             action_dim=cls.discrete_env.action_space.n,
#             is_discrete=True,
#             gpu=-1)

    # def test_get_action(self):
    #     continuous_vpg = VPG(
    #         state_shape=self.continuous_env.observation_space.shape,
    #         action_dim=self.continuous_env.action_space.low.size,
    #         is_discrete=False, gpu=-1)
    #     # continuous_obs = self.continuous_env.reset()
    #     action, log_pi = continuous_vpg.get_action(
    #         self.dummy_continuous_obs, test=False)
    #     self.assertEqual(action.ndim, 1)
    #     actions, log_pis = continuous_vpg.get_action(
    #         self.dummy_continuous_obses, test=False)
    #     self.assertEqual(actions.shape[1],
    #                      self.continuous_env.action_space.low.size)
    #     self.assertEqual(actions.shape[0],
    #                      self.batch_size)

    # def test_train(self):
    #     rewards = np.zeros(shape=(self.batch_size,), dtype=np.float32)
    #     dones = np.zeros(shape=(self.batch_size,), dtype=np.float32)
    #     log_pis = np.zeros(shape=(self.batch_size,), dtype=np.float32)

    #     print("Discrete test is not implemented yet")
    #     continuous_vpg = VPG(
    #         state_shape=self.continuous_env.observation_space.shape,
    #         action_dim=self.continuous_env.action_space.low.size,
    #         is_discrete=False, gpu=-1)
    #     continuous_acts = np.zeros(
    #         shape=(self.batch_size,)+self.continuous_env.action_space.shape,
    #         dtype=np.float32)
    #     continuous_vpg.train_actor(
    #         self.dummy_continuous_obses, continuous_acts,
    #         self.dummy_continuous_obses, rewards, dones, log_pis)
    #     continuous_vpg.train_critic(
    #         self.dummy_continuous_obses, continuous_acts,
    #         self.dummy_continuous_obses, rewards, dones)


if __name__ == '__main__':
    unittest.main()
