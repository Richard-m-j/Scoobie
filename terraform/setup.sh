
sudo su
hostnamectl set-hostname kmaster
kubeadm init
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
kubectl taint node kmaster node-role.kubernetes.io/control-plane:NoSchedule-
git clone https://github.com/Richard-m-j/Scoobie.git
