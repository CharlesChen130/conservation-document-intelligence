# Holdout v4 Freeze Manifest

- Question set: `data/holdout_v4_spec.yaml`
- Question count: 20 (`J01`–`J20`)
- Expected supported answers: 16
- Expected abstentions: 4
- First-run artifact prefix: `holdout_v4`
- Pre-run artifact state: answer report, checkpoint, metrics, and audit were all absent
- Policy: execute once without tuning retrieval, prompting, intent routing, answer validation, or fallback behavior against these questions

## Pre-run SHA-256 values

| Frozen input | SHA-256 |
|---|---|
| `data/holdout_v4_spec.yaml` | `ae3b8a644d7a979d9c874501caf71d6fc5178803722c0413b80eec41de21bb92` |
| `src/conservation_intelligence/chatbot.py` | `c6ba53de52a4afbfc308ee39d163ca33e2a81741ac011254622c6f5343cc10af` |
| `config.yaml` | `5b9da3b8e932013908cc96d6f0382e168d6af4eea7d5afadf4acb1eeac1eedfa` |
| `scripts/12_evaluate_fresh_holdout.py` | `d8fd71e0090ae69809f54d28c848d7dd5cfcdac69e83712de7b60e51ab7cc9a7` |

This manifest was created after validating the specification and before making any OpenAI request for this holdout. The first-run outputs are evaluation evidence and must not be overwritten or used for a repair/retest cycle.
