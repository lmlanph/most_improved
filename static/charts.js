    <script>

      {% for i in data_start %}

      const dataStart{{ loop.index0 }} = {
        datasets: [{
          backgroundColor: 'rgb(134, 204, 120)',
          borderColor: 'rgb(134, 204, 120, .45)',
          data: {{ data_start[loop.index0].chartScores | safe }}
        }]
      };

      const configStart{{ loop.index0 }} = {
        type: 'line',
        data: dataStart{{ loop.index0 }},
        options: {
          plugins: {
            legend: {
              display: false
              }
          },
          scales: {
            x: {
              offset: true,
              ticks: {
                display: false
              },
              parsing: false,
              type: 'time',
              min: '2015-01-01',
              max: '2021-12-28',
              time: {
                unit: 'year'
              }
            },
            y: {
              offset: true,
              beginAtZero: true,
              min: 0,
              max: 10
            }
          },
          responsive: false
        }
      };

      var myChartStart{{ loop.index0 }} = new Chart(
          document.getElementById('myChartStart{{ loop.index0 }}'),
          configStart{{ loop.index0 }}
        );
      {% endfor %}




      {% for i in data_end %}

      const dataEnd{{ loop.index0 }} = {
        datasets: [{
          backgroundColor: 'rgb(255, 177, 66)',
          borderColor: 'rgb(255, 201, 125, .45)',
          data: {{ data_end[loop.index0].chartScores | safe }}
        }]
      };

      const configEnd{{ loop.index0 }} = {
        type: 'line',
        data: dataEnd{{ loop.index0 }},
        options: {
          plugins: {
            legend: {
              display: false
              }
          },
          scales: {
            x: {
              offset: true,
              ticks: {
                display: false
              },
              parsing: false,
              type: 'time',
              min: '2015-01-01',
              max: '2021-12-28',
              time: {
                unit: 'year'
              }
            },
            y: {
              offset: true,
              beginAtZero: true,
              min: 0,
              max: 10
            }
          },
          responsive: false
        }
      };

      var myChartEnd{{ loop.index0 }} = new Chart(
          document.getElementById('myChartEnd{{ loop.index0 }}'),
          configEnd{{ loop.index0 }}
        );
      {% endfor %}


      function renderComment(t){
        // alert(t)
        var comment = t.querySelector('.hidden-comment').innerHTML;
        var score = t.querySelector('.hidden-score').innerHTML;
        var date = t.querySelector('.hidden-date').innerHTML;

        // var comments = comment.split(',');

        // for (let c of comment) {
        //   console.log(c)
        // };

        // console.log(typeof(comments))

        // for (const element of array1) {
        //   console.log(element);
        // }


        document.querySelector('.modal')
          .classList.toggle('modal-hidden');

        document.querySelector('.modal-text').innerHTML = comment;
        // alert(comment)
        // alert(score)
        // alert(date)
      };

      document.querySelector('.modal-close').addEventListener('click', closeModal);


      function closeModal(){
        document.querySelector('.modal').classList.toggle('modal-hidden')
      }





    </script>