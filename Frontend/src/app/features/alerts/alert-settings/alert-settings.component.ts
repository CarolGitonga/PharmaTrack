import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatChipsModule } from '@angular/material/chips';
import { AlertsService, AlertLog } from '../../../core/services/alerts.service';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-alert-settings',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatChipsModule,
  ],
  templateUrl: './alert-settings.component.html',
  styleUrl: './alert-settings.component.scss'
})
export class AlertSettingsComponent implements OnInit {
  private alertsService = inject(AlertsService);
  private auth = inject(AuthService);
  private snackBar = inject(MatSnackBar);

  user = this.auth.getUser();
  logs: AlertLog[] = [];
  loadingLogs = true;
  sendingTest = false;

  displayedColumns = ['medicine_name', 'alert_type', 'sent_to', 'sent_at', 'status'];

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.loadingLogs = true;
    this.alertsService.getLogs().subscribe({
      next: (data) => {
        this.logs = data;
        this.loadingLogs = false;
      },
      error: () => { this.loadingLogs = false; }
    });
  }

  sendTestSms(): void {
    this.sendingTest = true;
    this.alertsService.sendTestSms().subscribe({
      next: (res) => {
        this.snackBar.open(res.message, 'Close', { duration: 4000 });
        this.sendingTest = false;
        this.loadLogs();
      },
      error: (err) => {
        this.snackBar.open(err.error?.error || 'Failed to send SMS.', 'Close', { duration: 4000 });
        this.sendingTest = false;
      }
    });
  }

  getAlertTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      'LOW_STOCK': 'Low Stock',
      'EXPIRING_60': 'Expiring (60 days)',
      'EXPIRING_30': 'Expiring (30 days)',
      'EXPIRED': 'Expired',
    };
    return labels[type] || type;
  }
}
