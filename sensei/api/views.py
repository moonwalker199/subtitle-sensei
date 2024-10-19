from django.shortcuts import render, redirect
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import datetime
from .srt_extracter import extract_subtitles   # Import your AI subtitle extraction function
from .offset_calc import synchronize_srt       #Import your synchronization function


def upload_files(request):
    if request.method == 'POST' and request.FILES.get('file1') and request.FILES.get('incorrect_srt'):
        try:
            # Get the uploaded files
            video_file = request.FILES['file1']           # Video file
            incorrect_srt = request.FILES['incorrect_srt'] # Incorrect subtitles
            
            # Initialize FileSystemStorage
            fs = FileSystemStorage()
            
            # Save the uploaded files with timestamp to avoid name conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = fs.save(f'uploads/video_{timestamp}{os.path.splitext(video_file.name)[1]}', video_file)
            incorrect_srt_filename = fs.save(f'uploads/incorrect_{timestamp}.srt', incorrect_srt)
            
            # Get the full file paths
            video_path = os.path.join(settings.MEDIA_ROOT, video_filename)
            incorrect_srt_path = os.path.join(settings.MEDIA_ROOT, incorrect_srt_filename)
            
            # Generate AI subtitles using srt_extractor
            ai_generated_srt = f'uploads/ai_generated_{timestamp}.srt'
            ai_srt_path = os.path.join(settings.MEDIA_ROOT, ai_generated_srt)
            
            # Extract subtitles using AI
            extract_subtitles(video_path, ai_srt_path)
            
            # Create output filename for synchronized subtitles
            output_filename = f'synchronized_{timestamp}.srt'
            output_path = os.path.join(settings.MEDIA_ROOT, 'processed', output_filename)
            
            # Ensure the processed directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Synchronize the subtitles
            synchronize_srt(incorrect_srt_path, ai_srt_path, output_path)
            
            # Clean up temporary files
            fs.delete(video_filename)
            fs.delete(incorrect_srt_filename)
            fs.delete(ai_generated_srt)
            
            # Store the output path in session for the download view
            request.session['result_file_path'] = output_path
            
            # Redirect to download page
            return redirect('download_result')
            
        except Exception as e:
            return render(request, 'upload.html', {
                'error_message': f'Error processing files: {str(e)}'
            })
    
    return render(request, 'upload.html')

def download_result(request):
    result_file_path = request.session.get('result_file_path')
    
    if not result_file_path or not os.path.exists(result_file_path):
        return render(request, 'download.html', {
            'error_message': 'No processed file available for download.'
        })
    
    filename = os.path.basename(result_file_path)
    
    if request.method == 'POST':
        # Serve the file for download
        response = FileResponse(
            open(result_file_path, 'rb'),
            as_attachment=True,
            filename=filename
        )
        
        # Clean up the processed file after serving
        def cleanup_file(response):
            if os.path.exists(result_file_path):
                os.remove(result_file_path)
            return response
        
        response._resource_closers.append(cleanup_file)
        return response
    
    return render(request, 'download.html', {
        'filename': filename
    })