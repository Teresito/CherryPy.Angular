import { HttpClient } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';
import { componentState } from './componentService';


@Injectable()
export class apiServices {

    constructor(private httpClient: HttpClient, private state: componentState) { }

    public async listUserAPI(): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/onlineUsers`, null, { responseType: 'json' });
        this.checkResponse(response);
        return response['userList'];
    }

    public async pingAPI(): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/ping`, null, { responseType: 'text' });
        this.checkResponse(response);
        return response;
    }

    public loginAPI(user: String, pass: String) {
        return this.httpClient.post(`${webServer}/login`, { "user": user, "pass": pass }, { responseType: 'text' });
    }

    public async logoutAPI(): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/logout`, null, { responseType: 'text' });
        this.checkResponse(response);
        return response;
    }

    public async checkPrivateData(): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/check_privatedata`, null, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response
    }

    public async unlockData(uniqueKey: String): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/unlock_privatedata`, { 'decryptionKey': uniqueKey }, { responseType: 'text' });
        this.checkResponse(response);
        return response
    }

    public async newPrivateData(uniqueKey: String): Promise<any>  {
        let response = await this.httpClient.post(`${webServer}/add_pubkey`, { 'encryptionKey': uniqueKey }, { responseType: 'text' });
        this.checkResponse(response);
        return response;
    }
    // FOR NOW JUST ONE
    public async reportUser(): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/report_user`, null, { responseType: 'text' });
        this.checkResponse(response);
        return response;
    }

    public async broadcast(message: String): Promise<any> {
        let response = await this.httpClient.post(`${webServer}/broadcast`, { 'message': message }, { responseType: 'text' });
        this.checkResponse(response);
        return response;
    }

    public async get_broadcastMessages(): Promise<any> {
        let response = await this.httpClient.get(`${webServer}/get_publicMessages`, { responseType: 'json' }).toPromise()
        this.checkResponse(response);
        return response['public_messages'];
    }

    private checkResponse(response: any) {
        if (response == 2) {
            this.state.clearClient();
        }
    }

}