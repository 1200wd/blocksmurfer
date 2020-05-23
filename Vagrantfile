Vagrant.configure("2") do |config|
  config.vm.box = "kwilczynski/ubuntu-20.04-docker"
  config.vm.box_version = "0.1.0"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
end
