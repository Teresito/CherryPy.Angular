import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  listLoading = true;
  usersList = [];
  constructor(private API: apiServices) { }

  ngOnInit() {
    this.listLoading = true
    this.loadUsers()
  }

  loadUsers() {
    this.API.listUserAPI().then((response) => {
      for (let index = 0; index < response.length; index++) {
        response[index]['connection_updated_at'] = Date.now() - response[index]['connection_updated_at']*1000;
        this.usersList.push(response[index]);        
      }
      this.listLoading = false
    });
  }

  updateList(){
    this.listLoading = true;
    setTimeout(() => {
      this.loadUsers();
    }, 2500);
  }


  backToTop() {
    window.scrollTo(0, 0);
  }
}
