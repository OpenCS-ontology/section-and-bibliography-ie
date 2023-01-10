# section-and-bibliography-ie
Section &amp; bibliography information extraction

## Running

1. `docker build . -t [some name]:[some tag]` (it takes a while!)
2. Put your papers in `common` directory. The following commands assume that this directory is shared between your running container and host.
3. `docker run -v $(pwd)/common:/common [some name]:[some tag]`.
4. Run `docker ps` and check the name of your running container.
5. Attach to your container by executing `docker exec -it [name of running instance] bash`. Note that you can press TAB to get a hint on the name of your instance.
6. Now, you can call `./run.sh /path/to/your/pdf/file.pdf`. If you followed the commands above, the exemplary command might be `./run.sh /common/paper.pdf`. The output TTL will be produced in the same location.

Remark: You should be able to call `/s2orc-doc2json/run.sh` script from any directory, as it should resolve the paths correctly.
