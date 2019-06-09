import { Component, OnInit } from '@angular/core';
import { componentState } from '../services/componentService';
import { apiServices } from '../services/apiServices';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-privatemessage',
  templateUrl: './privatemessage.component.html',
  styleUrls: ['./privatemessage.component.css']
})
export class PrivatemessageComponent implements OnInit {

  message = new FormControl('');
  convoHistory: boolean = true;
  listLoading = true;
  usersList = [];
  messageList = [];
  selectedUser: any;
  loading = false;
  clickedUser = false;
  username: string;
  constructor(private state: componentState, private API: apiServices) { }

  ngOnInit() {
    this.username = sessionStorage.getItem('username');
    this.loadUsers();
    this.loadMessages();
  }


  loadMessages() {
    this.API.get_privateMessages().then((response) => {
      for (let i = 0; i < response.length; i++) {
        response[i][3] = response[i][3]*1000;
        
      }      
      this.messageList = response
      console.log(response)
    });
  }

  loadUsers() {
    this.API.listUserAPI().then((response) => {
      for (let index = 0; index < response.length; index++) {
        if (response[index]['username'] == sessionStorage.getItem('username')) {
          response.splice(index, 1);
        }
        else {
          response[index]['connection_updated_at'] = Date.now() - response[index]['connection_updated_at'] * 1000;
          this.usersList.push(response[index]);
        }
      }
      this.listLoading = false
    });
  }

  messageUser(userIndex: number) {
    this.clickedUser = true;
    this.selectedUser = this.usersList[userIndex];
    console.log(this.selectedUser)
  }

  onKeydown(event) {
    if (!this.loading) {
      this.sendMessage();
    }
  }

  sendMessage() {
    this.API.privatemessage(this.message.value, this.selectedUser.username, this.selectedUser.incoming_pubkey);
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
      this.message.patchValue(null);
    }, 2000);
  }

}
