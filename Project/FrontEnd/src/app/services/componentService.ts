import { Subject } from 'rxjs';

export class componentState {
    eKeyNotify = true;   
    loggedIn = false;
    loggedChanged = new Subject<any>();
}