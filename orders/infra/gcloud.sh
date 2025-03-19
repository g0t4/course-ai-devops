watch --no-title --color -- grc --colour=on kubectl get --show-kind pods

watch --no-title --color -- grc --colour=on kubectl top pod

watch --no-title --color -- grc --colour=on kubectl describe hpa

ab -n 3000 -c 10 EXTERNAL_SVC_IP:3000/order

watch --no-title --color -- grc --colour=on kubectl get --show-kind nodes
