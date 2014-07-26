Vagrant.configure("2") do |cnf|
  cnf.vm.box = "ubuntu/trusty64"
  cnf.vm.network :forwarded_port, guest: 8080, host: 8080
  cnf.vm.network :private_network, ip: "192.168.33.10"
  cnf.vm.synced_folder "./loslassa/projects/example", "/site"
  cnf.vm.provision :salt do |saltCnf|
      saltCnf.verbose = true
      saltCnf.minion_config = './salt/minion'
      saltCnf.run_highstate = true
      saltCnf.bootstrap_options = '-D'
      saltCnf.temp_config_dir = '/tmp'
  end
end
