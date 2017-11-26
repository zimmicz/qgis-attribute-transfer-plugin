build:
	rm -rf AttributeTransfer && \
	rm -f AttributeTransfer.zip && \
	mkdir AttributeTransfer && \
	find . ! -path "*/\.*" ! -path "./AttributeTransfer*" ! -path "." ! -path "*.pyc" -exec cp -r {} AttributeTransfer \; && \
	zip AttributeTransfer.zip ./AttributeTransfer/* && \
	rm -rf AttributeTransfer
