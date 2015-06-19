Name:           consul
Version:        0.5.2
Release:        2%{?dist}
Summary:        Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
Source0:        https://dl.bintray.com/mitchellh/%{name}/%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        https://dl.bintray.com/mitchellh/%{name}/%{version}_web_ui.zip
Source5:        %{name}.json
Source6:        %{name}-ui.json
Source7:        %{name}.logrotate
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%endif
Requires(pre): shadow-utils

%package ui
Summary: Consul Web UI
Group:   System Environment/Daemons
Requires: consul = %{version}

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%description ui
Consul comes with support for a beautiful, functional web UI. The UI can be used for viewing all services and nodes, viewing all health checks and their current status, and for reading and setting key/value data. The UI automatically supports multi-datacenter.

%prep
%setup -q -c -b 4

%install
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -D -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0644 %{S:1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -D -p -m 0644 %{S:5} %{buildroot}%{_sysconfdir}/%{name}.d/%{name}.json-dist
install -D -p -m 0644 %{S:6} %{buildroot}%{_sysconfdir}/%{name}.d/
install -D -p -m 0644 %{S:7} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d -m 0755 %{buildroot}/%{_datadir}/%{name}-ui/static
install -D -p -m 0644 dist/index.html %{buildroot}/%{_prefix}/share/%{name}-ui/
install -D -p -m 0644 dist/static/* %{buildroot}/%{_prefix}/share/%{name}-ui/static

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
  install -D -p -m 0644 %{S:2} %{buildroot}/%{_unitdir}/
%else
  install -D -p -m 0755 %{S:3} %{buildroot}/%{_initrddir}/%{name}
%endif

%pre
getent group consul >/dev/null || groupadd -r consul
getent passwd consul >/dev/null || \
    useradd -r -g consul -d /var/lib/consul -s /sbin/nologin \
    -c "consul.io user" consul
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(750,root,consul) %{_sysconfdir}/%{name}.d
%attr(640,root,consul) %{_sysconfdir}/%{name}.d/consul.json-dist
%dir %attr(750,consul,consul) %{_sharedstatedir}/%{name}
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/consul

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
  %attr(644,root,root) %{_unitdir}/%{name}.service
%else
  %attr(755,root,root) %{_initrddir}/%{name}
%endif

%files ui
%attr(-, root, consul) %{_prefix}/share/%{name}-ui
%config(noreplace) %attr(640,root,consul) %{_sysconfdir}/%{name}.d/consul-ui.json


%doc


%changelog
* Sat Jun 20 2015 PixelDrift.NET <support@pixeldrift.net> - 0.5.2-2
- Config init file to use root owned pid file
- Add logrotate for consul.log
- Add conditional restart for eL6 package upgrades
- Internal maintenance 

* Tue May 19 2015 nathan r. hruby <nhruby@gmail.com> - 0.5.2-1
- Bump to v0.5.2

* Fri May 15 2015 Dan <phrawzty@mozilla.com> - 0.5.1-1
- Bump to v0.5.1

* Mon Mar 9 2015 Dan <phrawzty@mozilla.com> - 0.5.0-2
- Internal maintenance (bump release)

* Fri Mar 6 2015 mh <mh@immerda.ch> - 0.5.0-1
- update to 0.5.0
- fix SysV init on restart
- added webui subpackage
- include statedir in package
- run as unprivileged user
- protect deployed configs from overwrites

* Thu Nov 6 2014 Tom Lanyon <tom@netspot.com.au> - 0.4.1-1
- updated to 0.4.1
- added support for SysV init (e.g. EL <7)

* Wed Oct 8 2014 Don Ky <don.d.ky@gmail.com> - 0.4.0-1
- updated to 0.4.0
