/**
 * @author Irving Popovetsky
 */

var windowheight = $(window).height() - 200;



jQuery(document).ready(function(){
  jQuery("#list").jqGrid({
    url:'/admin/data',
    datatype: 'json',
    jsonReader : { repeatitems: false },
    mtype: 'POST',
    colNames:[ 'Edit', 'Beer #', 'Beer Name', 'Brewery', 'Origin', '%ABV', 'Size', 'Unit of Measurement', 'Price $','On Tap', 'Link URL', 'Changed by', 'Line #', 'Date of last purchase', 'Cost per Oz', 'Freshest tapped Keg'],
    colModel :[
	{name:'act', index:'act', width:25, align:'center', sortable:false, search:false, formatter:'actions',
		formatoptions:{
			keys: true,
			editformbutton: true,
			editOptions:{height:550,width:800, closeAfterEdit:true, reloadAfterSubmit:true, savekey: [true,13], // navkeys: [true,38,40],
                afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json', search:false}); return [true]; }
            },
			delOptions:{reloadAfterSubmit:true,
                afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json', search:false}); return [true]; }
            }
        }
	},
	{name:'beerid', index:'beerid', width:55, search:false, hidden:true},
	{name:'name', index:'name', width:80, sortable:true, editable:true, edittype:'text', editoptions: {size:30, maxlength: 30}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} },
	{name:'brewery', index:'brewery', width:60, sortable:true, editable:true, edittype:'text', editoptions: {size:30, maxlength: 30}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} },
	{name:'origin', index:'origin', width:25, align:'center', sortable:true, editable:true, edittype:'text', editoptions: {size:20, maxlength: 20}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} },
	{name:'abv', index:'abv', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false },
	{name:'size', index:'size', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false },
	{name:'meas', index:'meas', width:25, align:'center', sortable:true, editable:true, edittype:'select', editoptions: {value: {oz:'oz',L:'L'}}, editrules: {required:true}, search:false },
	{name:'price', index:'price', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false },
	{name:'active', index:'active', width:25, align:'center', sortable:true, editable:true, edittype:'checkbox', editoptions: { value:"true:false" }, formatter:'checkbox', stype: 'select', searchoptions: { sopt:['eq','ne'], value:':All;true:Yes;false:No' }},
	{name:'url', index:'url', width:100, sortable:false, hidden: true, editable:true, edittype:'text', editoptions: {size:100,maxlength:150}, editrules: {edithidden: true, required:false} },
	{name:'bartender', index:'bartender', width:25, sortable:false, hidden: true, editable:true, edittype:'text', editoptions: {size:30,maxlength:50}, editrules: {edithidden: true, required:true} },
	{name:'lineno', index:'lineno', width:15, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:2, maxlength: 2}, editrules: {required:true, number:true}, search:true },
   	{name:'purdate', index:'purdate', width:30, align:'center',sortable:true, editable:true, formatter:'date', hidden: true,
	    formatoptions: {srcformat:'Y-m-d H:i:s', newformat:'Y-m-d'}, sorttype: 'datetime', editrules: {edithidden: true, required:true, date:true }, search:false,
	    editoptions: { dataInit:function(elm){setTimeout(function(){
                    jQuery(elm).datepicker({dateFormat:'yy-mm-dd'});
                    jQuery('.ui-datepicker').css({'width: 150px; font-size':'40%'});
		},200);}
	    }
	},
	{name:'costper', index:'costper', width:30, align:'center',sortable:true, hidden: true, editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {edithidden: true, required:true, number:true}, search:false },
	{name:'freshest', index:'freshest', width:30, align:'center', sortable:true, editable:true, edittype:'checkbox', editoptions: { value:"true:false" }, formatter:'checkbox', stype: 'select', searchoptions: { sopt:['eq','ne'], value:':All;true:Yes;false:No' }}
    ],
    pager: '#pager',
    rowNum: 50,
    rowTotal:2000,
    //scroll:1,
    hoverrows:false,
    loadonce:true,
    // automatically adjusting window height
    height: windowheight,
//    rowList:[100,200,300,400,500,600,700],
    sortname: 'brewery, name',
    sortorder: 'asc',
    viewrecords: true,
    autowidth: true,
    ignoreCase:true,
    editurl: "/admin/edit",
    caption: 'Beer Menu Administration',
    gridComplete: function(){ }
  });

    jQuery("#list").jqGrid('navGrid',"#pager",{search:false, edit:false, add:true, del:false,
            beforeRefresh: function () { resetme() }
        },
		   {}, // default settings for delete
		   {height:550,width:800, closeAfterEdit:true, reloadAfterSubmit:true, savekey: [true,13], // navkeys: [true,38,40],
               afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json',search:false}); return [true]; }
           }, // default settings for add
		   {}, //edit
		   {}, // search options
		   {}
);

    jQuery("#list").jqGrid('filterToolbar', {stringResult: false, searchOnEnter: false, defaultSearch : "cn"});

    function resetme() {
        var grid = $("#list");
        grid.jqGrid('setGridParam',{datatype: 'json', search:false});

        var postData = grid.jqGrid('getGridParam','postData');
        $.extend(postData,{filters:""});
        // for singe search you should replace the line with
        // $.extend(postData,{searchField:"",searchString:"",searchOper:""});

        // grid.trigger("reloadGrid",[{page:1}]);
        return [true];
    };
}); 