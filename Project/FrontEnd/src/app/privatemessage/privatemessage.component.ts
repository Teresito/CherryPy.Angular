import { Component, OnInit } from '@angular/core';
import { componentState } from '../services/componentService';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-privatemessage',
  templateUrl: './privatemessage.component.html',
  styleUrls: ['./privatemessage.component.css']
})
export class PrivatemessageComponent implements OnInit {

  convoHistory: boolean = true;
  listLoading = true;
  usersList = [];
  messageList = [];
  clickedUser = false;
  constructor(private state: componentState, private API: apiServices) { }

  ngOnInit() {
    this.loadUsers();
    this.loadMessages();
  }


  loadMessages() {
    this.API.get_privateMessages().then((response) => {      
      console.log(response)
      this.messageList = response
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
    console.log(this.usersList[userIndex]);
  }

}
