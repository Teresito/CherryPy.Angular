import { Component, OnInit } from '@angular/core';
import { AuthGuard } from '../services/auth-guard.service';
import { Router } from '@angular/router';
import { componentState } from '../services/componentService';

@Component({
  selector: 'app-page-not-found',
  templateUrl: './page-not-found.component.html',
  styleUrls: ['./page-not-found.component.css']
})
export class PageNotFoundComponent implements OnInit {

  constructor(private state: componentState, private route: Router) { }

  ngOnInit() {
    let auth = Boolean(sessionStorage.getItem('authenticated'));
    setTimeout(() => {
      if (auth){
        this.route.navigate(['/broadcast'])
      }
      else{
        this.route.navigate(['/login'])
      }
    },
      2000);

  }

}
