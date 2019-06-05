import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {

  constructor(private API: apiServices) { }

  ngOnInit() {

  }

  loadUser(){
    this.API.listUserAPI().subscribe(
      (response) => {
        console.log(JSON.parse(response));
      }

    );
  }

}
