import requests
import json
import getpass

#"""
#Modify these please
#"""
#switchuser='USERID'
#switchpassword='PASSWORD'

# ******************************************************
# **                                                  **
# **     This code was written by Rich Cordan aka     **
# ** RichTechGuy for the RichTechGuy YouTube Channel. **
# **                                                  **
# **    Some code was created via the NXAPI from a    **
# **              Cisco Nexus 9000 switch.            **
# **                                                  **
# **                www.richtechguy.com               **
# **            richtechguy@richtechguy.com           **
# **                                                  **
# ****************************************************** 

#    nxCall.py is designed to be imported into other python scripts that
#    need to send commands and receive data from Cisco Nexus 9000 series
#    switches.

#    Copyright (C) 2023  Rich Cordan

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#Send show command to Nexus switch, receive JSON response
def nxShow(user, passwd, addr, command):
  url='https://' + addr + '/ins'
  myheaders={'content-type':'application/json'}
  payload={
    "ins_api": {
      "version": "1.0",
      "type": "cli_show",
      "chunk": "0",
      "sid": "1",
      "input": command,
      "output_format": "json"
    }
  }
  response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(user,passwd)).json()

  return response["ins_api"]["outputs"]["output"]

#Send show command to Nexus switch and receive human readable response
def nxShow_h(user, passwd, addr, command):
  url='https://' + addr + '/ins'
  myheaders={'content-type':'application/json'}
  payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show_ascii",
    "chunk": "0",
    "sid": "1",
    "input": command,
    "output_format": "json"
    }
  }
  response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(user,passwd)).json()

  return response["ins_api"]["outputs"]["output"]["body"]


#Send config commands to Nexus switch and receive a list of dictionaries with http code responses for each command.
#Send multiple commands by seperating each command with ' ;' (Space before semicolon)
def nxConfig(user, passwd, addr, command):
  url='https://' + addr + '/ins'
  myheaders={'content-type':'application/json'}
  payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": command,
    "output_format": "json",
    "rollback": "rollback-on-error"
    }
  }
  response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(user,passwd)).json()

  return response["ins_api"]["outputs"]["output"]


if __name__ == "__main__":
  address = str(input("Enter the mgmt0 addres for the switch: "))
  username = str(input("Enter username: "))
  password = getpass.getpass(prompt='Password: ', stream=None)
  print("Enter the command(s)")
  print("For show commands, enter one command.")
  print("For configuration commands, enter all commands seperated by ' ;' - Space before semicolon.")
  command = str(input("Command: "))

  if command.lower()[0:2] == 'sh':

    nxResponse = nxShow(username, password, address, command)
    print("Command send to switch at " + address)
    print("Response: " + nxResponse["code"] + ", " + nxResponse["msg"])
    print(json.dumps(nxResponse["body"], indent=2))

    print(nxShow_h(username, password, address, command))

  else:
    nxResponse = nxConfig(username, password, address, command)
    for reply in nxResponse:
      print(reply["code"] + ", " + reply["msg"])