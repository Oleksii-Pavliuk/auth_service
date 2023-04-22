#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor




def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authenticate.settings')

    DjangoInstrumentor().instrument()
    LoggingInstrumentor().instrument()
    RequestsInstrumentor().instrument()



    jaeger_exporter = f"http://{os.environ.get('JAEGER_HOST')}:{os.environ.get('JAEGER_PORT')}/v1/traces"

    print(jaeger_exporter)
    
    trace.set_tracer_provider(TracerProvider(
        resource=Resource.create({
            SERVICE_NAME: "Authentication SERVICE"
    })
    ))
    span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=jaeger_exporter))
    trace.get_tracer_provider().add_span_processor(span_processor)


    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
