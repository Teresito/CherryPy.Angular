import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {

  constructor(private API: apiServices) { }

  ngOnInit() {
    this.API.pingAPI().subscribe(
      (response) => {
        console.log(response);
        console.log(typeof (response));
      }
    )

    this.API.endpointAPI().subscribe(
      (response) => {
        console.log(response);
      }
    )
  }

}
