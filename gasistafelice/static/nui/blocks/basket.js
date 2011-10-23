
jQuery.UIBlockBasketList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("basket", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
        this.submit_name = "Aggiorna il tuo paniere";
    },

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var iQta = 5;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"sWidth": "5%"},
                    {"sWidth": "5%"},
                    {"sWidth": "20%"},
                    {"sWidth": "30%"},
                    { "sType": "currency", "sClass": "taright", "sWidth": "10%" },
                    { "bSortable" : false, "sClass": "taright", "sWidth": "15%" ,
                      "fnRender": function ( oObj ) {
                                    var step = $(oObj.aData[iQta]).attr('step');
                                    var min =  $(oObj.aData[iQta]).attr('minimum_amount');
                                    var price =  parseFloat(oObj.aData[iQta-1].replace(',','.').replace('&#8364;',''));
                                    var rv = '<span class="hand" onclick="fncOrder($(this),-'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/remove.png"></span>'; 
                                    rv += oObj.aData[iQta];
                                    rv += '<span class="hand" onclick="fncOrder($(this),+'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/add.png"></span>';
                                    return rv
                                  },
                     },
                    { "sType": "currency", "bSortable" : false, "sClass": "taright", "sWidth": "10%" },
                    {"sWidth": "5%"}
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {

                    var iTotal = 0;
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][iQta+1].substr(8).replace(',','.'));
                    }
                    
                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + String(GetRoundedFloat(iTotal)).replace('.',','));

                }
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["basket"] = new jQuery.UIBlockBasketList();

