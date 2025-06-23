import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload.html',
  styleUrl: './upload.css'
})
export class Upload {
  selectedFile: File | null = null;
  uploading = false;
  uploadSuccess = false;
  uploadError = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.uploadSuccess = false;
    this.uploadError = '';
  }

  onUpload() {
    if (!this.selectedFile) return;
    this.uploading = true;
    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('/upload/', formData).subscribe({
      next: () => {
        this.uploading = false;
        this.uploadSuccess = true;
      },
      error: err => {
        this.uploading = false;
        this.uploadError = err.error?.detail || 'Upload failed';
      }
    });
  }
}
