<template>
  <div>
    <h1>Celery Test</h1>
    <button @click="sendRequest">Send Request</button>
    <!-- <button @click="sendResponse">Send Response</button> -->
    <p>{{ output }}</p> 
    <p>Attempt: {{ attempt }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CeleryTest',
  data() {
    return {
      output: '',
      attempt: 0
    };
  },
  methods: {
    async sendRequest() {
      const response = await axios.post('/api/celery/test');
      console.log(response.data);
      const task_id = response.data.task_id;

      let status = null;
      const intervalId = setInterval(async () => {
        const response2 = await axios.get(`/api/celery/status/${task_id}`);
        status = response2.data.status;
        if (status === 'SUCCESS') {
          const result = response2.data.result;
          console.log(result);
          this.output = result;
          clearInterval(intervalId);
        }
        else{
            this.output = 'Task is running...';
            this.attempt += 1;
        }
      }, 5000);
      
      
    },
    
  }
}
</script>
