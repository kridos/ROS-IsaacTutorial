# Practice: Kubernetes Robot Fleets

1. **Kill a Pod on purpose.** With both Deployments running, run
   `kubectl delete pod -n ros2-demo -l app=talker` and watch `kubectl get
   pods -n ros2-demo -w` — confirm a replacement Pod is created
   automatically, the self-healing behavior DEEP_DIVE.md contrasts with
   Chapter 21's docker-compose (which has no such automatic recovery).

2. **Scale up.** Change `talker-deployment.yaml`'s `replicas` to 3 and
   re-`kubectl apply`. Confirm three talker Pods start — then think
   through (and write a sentence on) what would actually happen to the
   listener's received messages with 3 talkers publishing on the same
   topic via host networking, given what Chapter 2 taught about
   pub/sub with multiple publishers.

3. **Break the pitfall, verify the fix.** Do demo/README.md's
   "Try it: break the pitfall on purpose" exercise, then restore
   `hostNetwork: true` yourself and confirm the listener's logs resume.

4. **Add a Service.** Even though this chapter's demo doesn't need one
   (host networking), create a `ClusterIP` Service for the talker
   Deployment anyway, and use `kubectl describe service` to understand
   what stable identity it provides — practice with the concept even
   where the demo's own networking choice bypasses needing it.

5. **Stretch:** add a `livenessProbe` to `listener-deployment.yaml` that
   checks the container process is alive, deliberately misconfigure it
   to fail, and watch Kubernetes restart the Pod repeatedly via `kubectl
   get pods -n ros2-demo -w` — a look at Kubernetes' health-checking
   layer beyond just "the process didn't crash."
