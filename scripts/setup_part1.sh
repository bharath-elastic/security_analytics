cp /home/ubuntu/lab_config/part1.kibana.yml /home/ubuntu/kibana/config/kibana.yml
echo "kibana.index: .kibana_$(uuidgen)" >> /home/ubuntu/kibana/config/kibana.yml
