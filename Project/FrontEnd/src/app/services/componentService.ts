import { Subject } from 'rxjs';
import { Injectable, Injector } from '@angular/core';
import { Router } from '@angular/router';

@Injectable()
export class componentState {

    clientState = new Subject<any>(); // Tell components that the user is logged in
    session = new Subject<any>(); // Used to tell component the user is in session
    searchTrigger = new Subject<string>(); // Tell component the user is searching
    usersList: any; // List of all the online users for components to use

    /* 
        COMPONENT INTERACTIONS
    */
    constructor(private route: Router){}
    // Sets session storage to user info 
    setClient(username: string, bool: boolean){
        sessionStorage.setItem('status', 'Online');
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('authenticated', bool.toString());
        this.route.navigate(['/broadcast'])
        this.clientState.next();
    }
    // Clear session storage to user info 
    clearClient(){
        sessionStorage.removeItem('status');
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('authenticated');
        sessionStorage.removeItem('inSession');
        this.route.navigate(['/login'])
        this.clientState.next();
        this.session.next();
    }

    getAuth(){
        return Boolean(sessionStorage.getItem('authenticated'));
    }

}