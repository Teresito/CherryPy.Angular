import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  messageLoading = true;
  usersList = [];
  constructor(private API: apiServices) { }

  ngOnInit() {
    this.messageLoading = true
    this.loadUsers()
  }

  loadUsers() {
    this.API.listUserAPI().then((response) => {
      for (let index = 0; index < response.length; index++) {
        response[index]['connection_updated_at'] = Date.now() - response[index]['connection_updated_at']*1000;
        this.usersList.push(response[index]);        
      }
      this.messageLoading = false
    });
  }

}
