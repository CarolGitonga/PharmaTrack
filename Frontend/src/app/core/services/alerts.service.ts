import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AlertLog {
  id: number;
  medicine: number;
  medicine_name: string;
  alert_type: string;
  message: string;
  sent_to: string;
  sent_at: string;
  was_successful: boolean;
}

@Injectable({ providedIn: 'root' })
export class AlertsService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  getLogs(): Observable<AlertLog[]> {
    return this.http.get<AlertLog[]>(`${this.apiUrl}/alerts/logs/`);
  }

  sendTestSms(): Observable<any> {
    return this.http.post(`${this.apiUrl}/alerts/test-sms/`, {});
  }
}
