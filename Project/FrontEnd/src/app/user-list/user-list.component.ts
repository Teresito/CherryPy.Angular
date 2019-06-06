import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {


  onlineUsers: any;
  timeWait: any;
  userLoading: boolean = true;
  constructor(private state: componentState) { }

  ngOnInit() {
    this.onlineUsers = this.state.onlineUsers;
    console.log(this.onlineUsers)
    if (this.onlineUsers == undefined){ // Initial login
      this.timeWait = setInterval(() => {
        if (this.onlineUsers != undefined) {
          clearInterval(this.timeWait);
          this.userLoading = false;
        }
        this.onlineUsers = this.state.onlineUsers;
      }, 2000);
    }
    else{
      this.userLoading = false;
    }

  }

}
