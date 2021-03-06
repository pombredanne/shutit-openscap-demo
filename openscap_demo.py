"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class openscap_demo(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#									to be seen before continuing. By default this is managed
		#									by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)- Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)- Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#									- Returns True if any lines in output match any of 
		#									the regexp strings in the matches list
		# shutit.send_until(send,regexps)	- Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)		- Run the passed-in string as a script
		# shutit.install(package)			- Install a package
		# shutit.remove(package)			 - Remove a package
		# shutit.login(user='root', command='su -')
		#									- Log user in with given command, and set up prompt and expects.
		#									Use this if your env (or more specifically, prompt) changes at all,
		#									eg reboot, bash, ssh
		# shutit.logout(command='exit')	- Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)		 - Add a line to bashrc
		# shutit.get_url(fname, locations)- Get a file via url from locations specified in a list
		# shutit.get_ip_address()			- Returns the ip address of the target
		# shutit.command_available(command)- Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#									Send a message to the log. add_final_message adds message to
		#									output at end of build
		# shutit.pause_point(msg='')		 - Give control of the terminal to the user
		# shutit.step_through(msg='')		- Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)- Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#									- Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#									- Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#									- Insert text into file fname after the first occurrence of 
		#									regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#									- Delete text from file fname after the first occurrence of
		#									regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#									- Replace text from file fname after the first occurrence of
		#									regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#									- Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#									- Returns True if file exists on target
		# shutit.user_exists(user)		- Returns True if the user exists on the target
		# shutit.package_installed(package)- Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#									- Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#									- Get input from user and return output
		# shutit.fail(msg)				- Fail the program and exit with status 1
		# 
		if shutit.file_exists('/tmp/docker_openscap',directory=True):
			shutit.send('cd /tmp/docker_openscap')
			shutit.send('vagrant destroy -f')
			shutit.send('cd -')
			shutit.send('rm -rf /tmp/docker_openscap')
		shutit.send('mkdir -p /tmp/docker_openscap')
		shutit.send('cd /tmp/docker_openscap')
		shutit.send('vagrant init ianmiell/centos7_lvm')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su')
		shutit.install('docker')
		shutit.install('openscap-utils')
		shutit.install('wget')
		shutit.send('systemctl start docker')

		# based on: https://blogs.oracle.com/darren/entry/compliance_reporting_with_scap
		oval_def = r'''<?xml version="1.0" encoding="UTF-8"?>
<oval_definitions xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:oval="http://oval.mitre.org/XMLSchema/oval-common-5" xmlns:oval-def="http://oval.mitre.org/XMLSchema/oval-definitions-5" xmlns:independent-def="http://oval.mitre.org/XMLSchema/oval-definitions-5#independent" xsi:schemaLocation="http://oval.mitre.org/XMLSchema/oval-definitions-5 oval-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-definitions-5#independent independent-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-common-5 oval-common-schema.xsd">
  <generator>
    <oval:product_name>Enhanced SCAP Editor</oval:product_name>
    <oval:product_version>0.0.11</oval:product_version>
    <oval:schema_version>5.8</oval:schema_version>
    <oval:timestamp>2015-12-12T21:43:55</oval:timestamp>
  </generator>
  <definitions>
    <definition id="oval:shutit.tk:def:1" version="1" class="compliance">
      <metadata>
        <title>OS Release</title>
        <affected family="unix">
          <platform>CentOS Linux 7</platform>
        </affected>
        <description>Check this is rhel</description>
      </metadata>
      <criteria operator="AND" negate="false" comment="Single test">
        <criterion comment="Include test." test_ref="oval:shutit.tk:tst:1" negate="false"/>
      </criteria>
    </definition>
  </definitions>
  <tests>
    <textfilecontent54_test xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#independent" id="oval:shutit.tk:tst:1" version="1" check="all" comment="Test object" check_existence="all_exist">
      <object object_ref="oval:shutit.tk:obj:1"/>
    </textfilecontent54_test>
  </tests>
  <objects>
    <textfilecontent54_object xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#independent" id="oval:shutit.tk:obj:1" version="1" comment="Test content">
      <path datatype="string" operation="equals">/etc</path>
      <filename datatype="string" operation="equals">os-release</filename>
      <pattern datatype="string" operation="pattern match">^.*centos.*$</pattern>
      <instance datatype="int" operation="greater than or equal">1</instance>
    </textfilecontent54_object>
  </objects>
</oval_definitions>'''
		shutit.send_file('/tmp/test1.xml',oval_def)
		shutit.send('cat /tmp/test1.xml',note='View the contents of our simple test, which is OK (true) if this is a centos machine.')
		shutit.send('oscap oval eval /tmp/test1.xml', note='We can evaluate this policy on the host with this command.')

		shutit.send('docker run -d --name "our-rhel7-container" -ti registry.access.redhat.com/rhel7 sleep infinity',note='Run up a rhel7 container in the background')
		shutit.send('oscap-docker image registry.access.redhat.com/rhel7 oval eval /tmp/test1.xml',note='Now perform the check we created earlier against the rhel image. It will fail (false), as it is not a CentOS image.')
		shutit.send('oscap-docker container-cve our-rhel7-container',note='Get a more general cve report for this container.')
		shutit.install('scap-security-guide',note='Install the ssg security policy')
		shutit.send('oscap-docker container our-rhel7-container oval eval --results oval-results.xml --report report.html /usr/share/xml/scap/ssg/content/ssg-rhel7-oval.xml',note='Scan the image with a custom security policy, and generate a report in html and xml.')
		shutit.send('cat oval-results.xml',note='Output the xml results')
		shutit.send('oscap-docker image registry.access.redhat.com/rhel7 oval eval --results oval-results.xml --report report.html /usr/share/xml/scap/ssg/content/ssg-rhel7-oval.xml',note='Do the same, but scan the image rather than the container.')
		shutit.pause_point('')

		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#									- Get configuration value, boolean indicates whether the item is 
		#									a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#									and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return openscap_demo(
		'tk.shutit.openscap_demo.openscap_demo.openscap_demo', 1152822319.0001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)

