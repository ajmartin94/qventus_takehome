"""Adapters: implementations of the ports.

Only the composition root (`or_booking.app`) imports from here. Fixture-backed
adapters read the simulated hospital in `fixtures/`; stub adapters return a
structured "not supported" result or record what they would have done, and never
pretend to succeed.
"""
