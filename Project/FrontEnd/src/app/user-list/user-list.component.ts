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


  }

}
