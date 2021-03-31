Vagrant.configure("2") do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.vm.define "server" do |server|
    server.vm.box = "ubuntu/focal64"
    server.vm.network "private_network", ip: "192.168.1.30", bridge: 'wlo1'
    server.vm.hostname = "server"
    server.hostmanager.aliases = %w(server.poly.puppet.com)
    server.vm.provider :virtualbox do |vb|
        vb.name = "server"
        vb.memory = 2048
        vb.cpus = 3
    end
    server.vm.provision "shell", inline: "apt-get -y install make"
    server.vm.provision "shell", inline: "cd /vagrant && make server"
  end

  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.network "private_network", ip: "192.168.1.31", bridge: 'wlo1'
    ubuntu.vm.provider :virtualbox do |vb|
        vb.name = "ubuntu"
        vb.memory = 512
        vb.cpus = 1
    end
    ubuntu.vm.provision "shell", inline: "apt-get -y install make"
    ubuntu.vm.provision "shell", inline: "cd /vagrant && make agent"
  end

  #config.vm.define "windows" do |windows|
    #windows.vm.box = "gusztavvargadr/windows-server"
    #windows.vm.network "public_network", ip: "192.168.1.32", bridge: 'wlo1'
    #windows.vm.provider :virtualbox do |vb|
        #vb.name = "windows"
        #vb.memory = 1536
        #vb.cpus = 1
    #end
  #end

end
