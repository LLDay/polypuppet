Vagrant.configure("2") do |config|
  config.hostmanager.enabled = false
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.hostmanager.ip_resolver = proc do |machine|
    result = ""
    machine.communicate.execute("ip addr show enp0s8") do |type, data|
        result << data if type == :stdout
    end
    (ip = /inet (\d+\.\d+\.\d+\.\d+)/.match(result)) && ip[1]
  end

  config.vm.define "s" do |server|
    server.vm.box = "ubuntu/focal64"
    server.vm.network "public_network", ip: "192.168.0.30"
    server.vm.hostname = "polypuppet.duckdns.org"
    server.hostmanager.aliases = %w(polypuppet.duckdns.org)
    server.vm.provider :virtualbox do |vb|
        vb.name = "server"
        vb.memory = 3072
        vb.cpus = 2
    end
    server.vm.network "forwarded_port", guest: 80, host: 80
    server.vm.network "forwarded_port", guest: 443, host: 443
    server.vm.network "forwarded_port", guest: 8139, host: 8139
    server.vm.network "forwarded_port", guest: 8140, host: 8140
    server.vm.network "forwarded_port", guest: 22, host: 2000
    server.vm.provision "shell", inline: "apt-get -y install make"
    server.vm.provision "shell", inline: "sed -i 's#127.0.2.1#192.168.0.30#' /etc/hosts"
    server.vm.provision "shell", inline: "cd /vagrant && make server"
  end

  config.vm.define "u" do |ubuntu|
    ubuntu.vm.box = "ubuntu/focal64"
    ubuntu.vm.network "public_network", ip: "192.168.0.31"
    ubuntu.vm.network "forwarded_port", guest: 22, host: 2001
    ubuntu.vm.provider :virtualbox do |vb|
        vb.name = "ubuntu"
        vb.memory = 768
        vb.cpus = 1
    end
    ubuntu.vm.synced_folder ".", "/etc/puppetlabs/code/environments/production/"
    ubuntu.vm.provision "shell", inline: "apt-get -y install make"
    ubuntu.vm.provision "shell", inline: "cd /etc/puppetlabs/code/environments/production && make agent"
  end

  config.vm.define "windows" do |windows|
    windows.vm.box = "gusztavvargadr/windows-10"
    windows.vm.network "public_network", ip: "192.168.1.32"
    windows.vm.network "forwarded_port", guest: 22, host: 2002
    windows.vm.provider :virtualbox do |vb|
        vb.name = "windows"
        vb.memory = 1536
        vb.cpus = 1
    end
  end

end
