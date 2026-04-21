import logging
from celery import shared_task
from django.core.files.base import ContentFile
from .models import RenderJob
from .render_pipeline import RenderPipeline

logger = logging.getLogger(__name__)

@shared_task
def process_render_job(job_id):
    try:
        job = RenderJob.objects.get(id=job_id)
        job.status = 'processing'
        job.progress = 10
        job.save()

        # Initialize Pipeline
        pipeline = RenderPipeline(
            job.selected_view.base_image.path,
            job.uploaded_design.path
        )
        job.progress = 30
        job.save()

        # Run rendering
        output_bytes = pipeline.generate(
            job.selected_view.print_x,
            job.selected_view.print_y,
            job.selected_view.print_width,
            job.selected_view.print_height,
            job.selected_view.angle_type
        )
        job.progress = 90
        job.save()

        # Save output
        filename = f"render_v2_{job.id}.jpg"
        job.output_image.save(filename, ContentFile(output_bytes), save=False)
        job.status = 'completed'
        job.progress = 100
        job.save()
        
        return f"Job {job_id} rendered with high-fidelity pipeline."

    except Exception as e:
        logger.error(f"Render engine failure for job {job_id}: {str(e)}", exc_info=True)
        try:
            job = RenderJob.objects.get(id=job_id)
            job.status = 'failed'
            job.error_message = f"Render Error: {str(e)}"
            job.save()
        except:
            pass
        return f"Job {job_id} failed."
