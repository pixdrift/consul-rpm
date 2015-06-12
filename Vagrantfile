# -*- mode: ruby -*-
# vi: set ft=ruby :

$rpmbuild_script = <<SCRIPT

echo "Provisioning started, installing packages..."
sudo yum -y install epel-release
sudo yum -y install rpmdevtools mock

if grep -q -i "release 5" /etc/redhat-release ; then
  echo '%dist .el5' > ~/.rpmmacros
  echo '%_sharedstatedir /var/lib' >> ~/.rpmmacros
  if [ ! "$(wget --version | head -1 | cut -d' ' -f3)" = "1.16" ]; then
    sudo yum -y install openssl-devel
    sudo /sbin/ldconfig
    if [ ! -d wget-1.16 ] ; then
      wget http://ftp.gnu.org/gnu/wget/wget-1.16.tar.gz
      tar -xzvf wget-1.16.tar.gz
    fi
    cd wget-1.16
    ./configure --with-ssl=openssl --with-libssl-prefix=/usr/lib64/ --prefix=/usr
    make
    sudo make install
    cd -
  fi
fi

echo "Setting up rpm dev tree..."
rpmdev-setuptree

echo "Linking files..."
ln -s /vagrant/SPECS/consul.spec $HOME/rpmbuild/SPECS/
find /vagrant/SOURCES -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \\;

echo "Downloading dependencies..."
spectool -g -R rpmbuild/SPECS/consul.spec

echo "Building rpm..."
rpmbuild -ba rpmbuild/SPECS/consul.spec

echo "Copying rpms back to shared folder..."
find $HOME/rpmbuild -type d -name "RPMS" -exec cp -r {} /vagrant/ \\;
find $HOME/rpmbuild -type d -name "SRPMS" -exec cp -r {} /vagrant/ \\;

SCRIPT


Vagrant.configure(2) do |config|

  config.vm.box = ""

  config.vm.provision "shell", inline: $rpmbuild_script, privileged: false

end
