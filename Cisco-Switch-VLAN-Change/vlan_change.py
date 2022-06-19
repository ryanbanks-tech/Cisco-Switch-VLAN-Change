import csv, re, os
from dotenv import load_dotenv
from jinja2 import Template
from tqdm import tqdm
from Switch import *

# Loads our environment variables
load_dotenv()

print("""
                       #@&*                                                    
                  .@@@@@@@@@@@@@%   #@@@@@@@@@@@(                               
                @@@@#          @@@@@@@.        @@@@@   *@@@&,                   
              %@@@                                #@@@@@@##@@@@@@               
             #@@#                                              /@@@@@@@%.       
            /@@%                                                  ,/. .&@@@@    
           /@@&,,                                                         /@@*  
          @@@#  @                                                          .@@  
         @@@   *@              #  (*                                        &@@ 
       #@@&    %@               @@.            ,   .                        .@@ 
     *@@@      @@               @               &@@                          @@ 
   %@@@        @@               @               ,@                           &@/
 (@@@          @@              /@               #@               @@          .@@
,@@            @@              &@               @@              /%            @@
@@@            &@,             @@               @&              @/            #@
 @@#            @@@*          ,@(              .@&             .@.            &@
  @@@#          (@, .         @@               (@*             %@             @#
    #@@*         #@@@* *((*  %@@               @@              @#            @& 
      @@@     ,@&(%@@@@@@@@@@@@@    /(         @@             &@            @(  
        @@#&#       .@@@@@@@#@@@@#  ,,  *%@&# /@%            .@&          *@.   
         @@%  .#  #            @@@@@@@&*. %@@@@@   .@@@@(.   @@          (@     
          ,@@@  (.          *##.   @@@@@@@@@@@@@& ,@(/@@@@@@@@@@#  ,/,  *@      
              #@@@@%     (       %. @@@@@@@@@@@@@@@@@@@@@@@@@@@@&**@@(,&#       
                     %@@@,       &. @          *(#(/.  ,@@@@@@@@@@@@*           
                          ,@@&  @*,@                                            
""")
print()
print("LET'S GET TO IT!")
print()

# Empty dictionary and lists to interact with our input file
input_dic = {}
network_list = []
switch_list = []
telnet_list = []

print("Getting env variables...\n")

# The jinja template will be used to compare interface configuration
template_file = os.getenv('JINJA_TEMPLATE')

WHATS_YOUR_NAME = os.getenv('T0_USERNAME')
TONY = os.getenv('T0_PASSWORD')

# Bringing in the input file
with open(os.getenv('INPUT_FILE')) as i:
    easyRead = csv.reader(i)
    readData = list(easyRead)
    for list in readData:
        (key, value) = (list[0], list[1])
        input_dic[key] = value

print("Parsing through the input file...\U0001f600\n")

# Using regex to match the first 2 letters of the word in the A column
def almost_there():
    newbie = re.findall('^\w\w', key)
    if newbie[0] == 'ne':
        network_list.append(input_dic[key])
    elif newbie[0] == 'sw':
        switch_list.append(input_dic[key])
    elif newbie[0] == 'te':
        telnet_list.append(input_dic[key])

for key in input_dic:
    almost_there()

# Setting variables for Netmiko
device_type = 'cisco_ios'
device_type_telnet = 'cisco_ios_telnet'
ssh_port = 22
telnet_port = 23
username = WHATS_YOUR_NAME
password = TONY

print("Now the work begins!\n")

# Opening our jinja template with a context manager
with open(template_file) as temp_file:
  int_template = Template(temp_file.read(), keep_trailing_newline = True)

# Iterates over each entry in our telnet list and displays a progress bar 
for idx, what_r_u in enumerate(tqdm(telnet_list, desc = "Telnet Switch Progress")):

  telnet_switch = Switch(device_type_telnet, what_r_u, WHATS_YOUR_NAME, TONY, telnet_port)
  telnet_switch.hostname = telnet_switch.get_prompt() 
  telnet_switch.got_data = telnet_switch.show_int_switchport()
  telnet_switch.switch_config = ""

  # Iterates through the list of dictionaries that our ntc template gives us for our output
  for index, intf in enumerate(telnet_switch.got_data):

    # The jinja template is rendered and compared
    int_config = int_template.render(
      vlan = '555',
      vader_voice = '99',
      access_vlan = intf['access_vlan'],
      admin_mode = intf['admin_mode'],
      interface = intf['interface'],
      mode = intf['mode'],
      switchport = intf['switchport'],
      switchport_monitor = intf['switchport_monitor'],
      switchport_negotitation = intf['switchport_negotiation'],
      trunking_vlans = intf['trunking_vlans'],
      voice_vlan = intf['voice_vlan']
    )

    # The changes that come from the jinja template are placed in the telnet switch config string to be used later
    telnet_switch.switch_config += int_config

  # Can use this create text files of the switch config before sending the instructions but the sending instructions will need to be commented out
  # with open(f"{telnet_switch.hostname}.txt", 'w') as file:
  #   file.write(telnet_switch.switch_config)

  # This will print the config in the console if you would rather see it there instead of a text file
  # print(f"\nThese are the changes for {telnet_switch.hostname}\n\n{telnet_switch.switch_config}")

  # This splits the switch config by a line break in order to send to the switch
  telnet_switch.instructions = telnet_switch.switch_config.split('\n')

  # This is a basic show command for proof of concept that the script is functioning properly without actually changing configuration
  # This will be commented out once comfortable the script functions like it should
  telnet_switch.test_instructions = "do show ip interface brief"

  # This prints the switch instructions that jinja generates in order for you to view the commands that will be sent
  # print(telnet_switch.instructions)

  # This prints the test instructions to view as proof of concept while the script runs
  # print(telnet_switch.send_instructions(telnet_switch.test_instructions))

  # This is the test that will be commented out once ready to send actual instructions
  telnet_switch.send_instructions(telnet_switch.test_instructions)

  # This is the actual config change that needs to be un-commented once ready 
  # telnet_switch.send_instructions(telnet_switch.instructions)

# The below code is for the ssh switch list and it funcions just as the telnet code above
for idx2, what_r_u2 in enumerate(tqdm(switch_list, desc = "SSH Switch Progress")):

  ssh_switch = Switch(device_type, what_r_u2, WHATS_YOUR_NAME, TONY, ssh_port)
  ssh_switch.hostname = ssh_switch.get_prompt() 
  ssh_switch.got_data = ssh_switch.show_int_switchport()
  ssh_switch.switch_config = ""

  for index2, intf2 in enumerate(ssh_switch.got_data):

    int_config = int_template.render(
      vlan = '555',
      vader_voice = '99',
      access_vlan = intf['access_vlan'],
      admin_mode = intf['admin_mode'],
      interface = intf['interface'],
      mode = intf['mode'],
      switchport = intf['switchport'],
      switchport_monitor = intf['switchport_monitor'],
      switchport_negotitation = intf['switchport_negotiation'],
      trunking_vlans = intf['trunking_vlans'],
      voice_vlan = intf['voice_vlan']
    )

    ssh_switch.switch_config += int_config

  # with open(f"{ssh_switch.hostname}.txt", 'w') as file:
  #   file.write(ssh_switch.switch_config)

  # print(f"\nThese are the changes for {ssh_switch.hostname}\n\n{ssh_switch.switch_config}")

  ssh_switch.instructions = ssh_switch.switch_config.split('\n')
  ssh_switch.test_instructions = "do show ip interface brief"

  # print(ssh_switch.instructions)
  # print(ssh_switch.send_instructions(ssh_switch.test_instructions))
  ssh_switch.send_instructions(ssh_switch.test_instructions)
  # ssh_switch.send_instructions(ssh_switch.instructions)

