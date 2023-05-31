//
//
// 在 JavaScript 文件中编写 JavaScript 代码
// var button = document.getElementById("button");
// var heading = document.getElementById("heading");
//
// button.addEventListener("click", function() {
//   heading.innerHTML = "Hello, World!";
// });
// var courseList = [
//     ['大学英语(Ⅳ)@10203', '大学英语(Ⅳ)@10203', '', '', '', '', '毛概@14208', '毛概@14208', '', '', '', '选修'],
//     ['', '', '信号与系统@11302', '信号与系统@11302', '模拟电子技术基础@16204', '模拟电子技术基础@16204', '', '', '', '', '', ''],
//     ['大学体育(Ⅳ)', '大学体育(Ⅳ)', '形势与政策(Ⅳ)@15208', '形势与政策(Ⅳ)@15208', '', '', '电路、信号与系统实验', '电路、信号与系统实验', '', '', '', ''],
//     ['', '', '', '', '电装实习@11301', '电装实习@11301', '', '', '', '大学体育', '大学体育', ''],
//     ['', '', '数据结构与算法分析', '数据结构与算法分析', '', '', '', '', '信号与系统', '信号与系统', '', ''],
//   ];
// document.addEventListener('DOMContentLoaded', function() {
//             var dataElement = document.getElementById('dataField');
//             if (dataElement) {
//                 var courseList = JSON.parse(dataElement.getAttribute('data-value'));
//                 // 处理返回的列表数据
//                 console.log(courseList);  // 示例：将列表数据打印到控制台
//             }else {
//               console.log('errorrrrrrrrrrrrrrrrrrrrrrrrrrr');
//             }
//         });
var dataElement = document.getElementById('dataField');
if (dataElement) {console.log('gooooooooooooooooooooooooood');}
console.log(dataElement);
if (dataElement) {console.log('gooooooooooooooooooooooooood');}
var courseList = JSON.parse(dataElement.getAttribute('data-value'));
// 处理返回的列表数据
console.log(courseList);  // 示例：将列表数据打印到控制台



  // var week = window.innerWidth > 360 ? ['周一', '周二', '周三', '周四', '周五'] :
  //   ['一', '二', '三', '四', '五'];
    var week = window.innerWidth > 360 ? ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] :
    ['一', '二', '三', '四', '五', '六', '日'];
  var day = new Date().getDay();
  var courseType = [
    [{index: '1', name: '8'}, 1],
    [{index: '2', name: '9'}, 1],
    [{index: '3', name: '10'}, 1],
    [{index: '4', name: '11'}, 1],
    [{index: '5', name: '12'}, 1],
    [{index: '6', name: '14'}, 1],
    [{index: '7', name: '15'}, 1],
    [{index: '8', name: '16'}, 1],
    [{index: '9', name: '17'}, 1],
    [{index: '10', name: '18'}, 1],
    [{index: '11', name: '19'}, 1],
    [{index: '12', name: '20'}, 1]
  ];
  // 实例化(初始化课表)
  var Timetable = new Timetables({
    el: '#coursesTable',
    timetables: courseList,
    week: week,
    timetableType: courseType,
    highlightWeek: day,
    gridOnClick: function (e) {
      alert(e.name + '  ' + e.week + ', 第' + e.index + '节课, 课长' + e.length + '节');
      console.log(e);
    },
    styles: {
      Gheight: 50
    }
  });
  // //切换课表
  // function onChange() {
  //   var courseListOther = [
  //     ['', '', '', '', '毛概@14208', '毛概@14208', '', '', '', '选修', '', ''],
  //     ['大学英语(Ⅳ)@10203', '大学英语(Ⅳ)@10203', '', '', '模拟电子技术基础@16204', '模拟电子技术基础@16204', '', '', '', '', '', ''],
  //     ['', '', '信号与系统@11302', '信号与系统@11302', '', '', '电路、信号与系统实验', '电路、信号与系统实验', '', '', '', ''],
  //     ['形势与政策(Ⅳ)@15208', '形势与政策(Ⅳ)@15208', '', '', '电装实习@11301', '电装实习@11301', '', '', '', '大学体育', '大学体育', ''],
  //     ['大学体育(Ⅳ)', '大学体育(Ⅳ)', '', '', '数据结构与算法分析', '数据结构与算法分析', '', '', '信号与系统', '信号与系统', '', ''],
  //   ];
  //
  //   Timetable.setOption({
  //     timetables: courseListOther,
  //     week: ['一', '二', '三', '四', '五', '六', '日'],
  //     styles: {
  //       palette: ['#dedcda', '#ff4081']
  //     },
  //     timetableType: courseType,
  //     gridOnClick: function (e) {
  //       console.log(e);
  //     }
  //   });
  // }