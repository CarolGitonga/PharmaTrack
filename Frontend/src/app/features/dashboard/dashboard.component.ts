import { Component, inject, OnInit, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Chart, registerables } from 'chart.js';
import { AuthService } from '../../core/auth/auth.service';
import { DashboardService, DashboardSummary } from '../../core/services/dashboard.service';
import { MedicineService } from '../../core/services/medicine.service';

Chart.register(...registerables);

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
    CurrencyPipe,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit, AfterViewInit {
  private auth = inject(AuthService);
  private dashboardService = inject(DashboardService);
  private medicineService = inject(MedicineService);

  @ViewChild('stockChart') stockChartRef!: ElementRef;

  user = this.auth.getUser();
  summary: DashboardSummary | null = null;
  loading = true;
  chart: Chart | null = null;

  ngOnInit(): void {
    this.dashboardService.getSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
        setTimeout(() => this.buildChart(), 0);
      },
      error: () => { this.loading = false; }
    });
  }

  ngAfterViewInit(): void {}

  buildChart(): void {
    this.medicineService.getAll().subscribe({
      next: (medicines) => {
        const top10 = medicines
          .sort((a, b) => b.quantity - a.quantity)
          .slice(0, 10);

        if (this.stockChartRef) {
          this.chart = new Chart(this.stockChartRef.nativeElement, {
            type: 'bar',
            data: {
              labels: top10.map(m => m.name),
              datasets: [{
                label: 'Current Stock',
                data: top10.map(m => m.quantity),
                backgroundColor: '#1565C0',
                borderRadius: 4,
              }]
            },
            options: {
              responsive: true,
              plugins: { legend: { display: false } },
              scales: { y: { beginAtZero: true } }
            }
          });
        }
      }
    });
  }

  logout(): void {
    this.auth.logout();
  }
}
