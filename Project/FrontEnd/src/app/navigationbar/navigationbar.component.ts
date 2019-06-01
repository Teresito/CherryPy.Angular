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
    this.state.loggedChanged.subscribe(
        ()=>{
          this.zIndex = this.state.eKeyNotify      
        }
      );
    
  }

  logout(){  
    this.api.logoutAPI().subscribe(
      (response)=>{
        if (response === 1){
          this.router.navigate(['/login']);
          this.state.setLoggedIn(false);
          this.state.deleteSession();
          this.state.eKeyNotify = true;
          this.state.loggedChanged.next();
        }
      }
    );
  }


}
