import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../core/auth/auth.service';
import { DashboardService, DashboardSummary } from '../../core/services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  private auth = inject(AuthService);
  private dashboardService = inject(DashboardService);

  user = this.auth.getUser();
  summary: DashboardSummary | null = null;
  loading = true;
  today = new Date();

  ngOnInit(): void {
    this.dashboardService.getSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: () => { this.loading = false; },
    });
  }

  get healthyCount(): number {
    if (!this.summary) return 0;
    const unhealthy = this.summary.low_stock_count + this.summary.expiring_soon_count + this.summary.expired_count;
    return Math.max(0, this.summary.total_medicines - unhealthy);
  }

  barWidth(count: number): string {
    const total = this.summary?.total_medicines || 1;
    return `${(count / total) * 100}%`;
  }

  formatStockValue(value: number): string {
    if (value >= 1_000_000) return (value / 1_000_000).toFixed(2) + 'M';
    if (value >= 1_000) return (value / 1_000).toFixed(1) + 'K';
    return value.toLocaleString('en-KE');
  }
}
