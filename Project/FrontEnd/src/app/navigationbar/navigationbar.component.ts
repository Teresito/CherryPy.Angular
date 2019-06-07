import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { apiServices } from '../services/apiServices';
import { AuthGuard } from '../services/auth-guard.service';
import { componentState } from '../services/componentService';

@Component({
  selector: 'app-navigationbar',
  templateUrl: './navigationbar.component.html',
  styleUrls: ['./navigationbar.component.css']
})
export class NavigationbarComponent implements OnInit {

  zIndex: boolean = true;

  constructor(private router: Router, private api: apiServices, private state: componentState) { }

  ngOnInit() {
    this.state.session.subscribe(
        ()=>{
        this.zIndex = !this.state.inSession;
        }
      );
    this.state.loggedChanged.subscribe(
      ()=>{
        if(this.state.getLoggedIn()==false){
          this.state.logout();
          this.router.navigate(['/login'])
        }
      }
    );
  }

  logout(){  
    this.state.logout();
  }


}
