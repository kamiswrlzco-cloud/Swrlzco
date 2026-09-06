# INT-CHAT-039J — Candidate v2 Handoff

The CLIENT CFv2.1.19 adaptive Chat candidate was repaired from workflow `30306467282` evidence. The only compiler blocker reported by that run was the missing `ExperimentalMaterial3Api` opt-in on the new provider-mesh bottom sheet. Candidate v2 fixes that blocker and adds a regression precheck for known Compose experimental-API opt-ins.

The CLIENT remains a candidate until a complete Android compile/debug build succeeds. SERVER testing is intentionally deferred because the operator is validating one component at a time.
