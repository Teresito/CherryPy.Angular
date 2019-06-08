import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {


  usersList = [];
  userLoading: boolean = true;

  constructor(private state: componentState,private API: apiServices) { }

  ngOnInit() {
    this.userLoading = false;
    this.loadUsers();
  }

  loadUsers() {
    this.API.listUserAPI().then((response) => {
      for (let index = 0; index < response.length; index++) {
        response[index]['connection_updated_at'] = Date.now() - response[index]['connection_updated_at'] * 1000;
        this.usersList.push(response[index]);
      }
      this.userLoading = false
    });
  }
}

