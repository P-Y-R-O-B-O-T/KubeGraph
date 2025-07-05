# KubeGraph

## Development & Testing
* Run the stacks
```bash
./test.sh
```
* Copy your `KUBECONFIG` in `/kubeconf` directory

### If facing any docker volume issues
```bash
sudo docker kill $(sudo docker ls -qa)
sudo docker container rm $(sudo docker container ls -aq)
sudo docker volume rm $(sudo docker volume ls -q)
./test.sh
```
