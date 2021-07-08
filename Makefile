.PHONY: all
all: 9606.protein.links.v11.0.txt.gz proteins_w_domains.txt barplot_appbio.png

9606.protein.links.v11.0.txt.gz:
	curl https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz > 9606.protein.links.v11.0.txt.gz

proteins_w_domains.txt:
	curl -L https://stockholmuniversity.box.com/shared/static/n8l0l1b3tg32wrzg2ensg8dnt7oua8ex > proteins_w_domains.txt

barplot_appbio.png: appbioproject.py

	python appbioproject.py
