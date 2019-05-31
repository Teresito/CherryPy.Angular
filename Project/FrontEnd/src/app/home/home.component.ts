import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  providers: [apiServices],
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private API: apiServices) { }

  ngOnInit() {
    this.API.pingAPI().subscribe(
      (response) => {
        console.log(response);
        console.log(typeof (response));
      }
    )
  }

}
