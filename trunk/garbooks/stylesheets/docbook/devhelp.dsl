<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!ENTITY dbstyle SYSTEM "docbook.dsl" CDATA DSSSL>
]>

<style-sheet>

<style-specification use="docbook">
<style-specification-body> 

;; These are some customizations to the Modular DocBook Stylesheets to produce
;; devhelp spec files.
;;
;; José Fonseca


(define %devhelp-name%
  ;; name of the devhelp book
  "")

(define %devhelp-version%
  ;; version of the devhelp book
  "")

;; Don't generate Table of Contents

(define ($generate-chapter-toc$) #f)
(define ($generate-qandaset-toc$) #f)

(define %generate-article-toc% #f)
(define %generate-book-toc% #f)
(define %generate-part-toc% #f)
(define %generate-reference-toc% #f)
(define %generate-set-toc% #f)

;; Stylesheet customization (taken from ldp.dsl)

(define %html-ext%
  ;; when producing HTML files, use this extension
  ".html")

(define (chunk-skip-first-element-list)
  ;; forces the Table of Contents on separate page
  '())

(define %root-filename%
  ;; The filename of the root HTML document (e.g, "index").
  "index")

(define %use-id-as-filename%
  ;; Use ID attributes as name for component HTML files?
  #t)


;; Table of Contents generation (based on dbautoc.dsl, v1.76)

(define (devhelp-toc-depth)
  10)

(define (build-devhelp-toc nd depth #!optional (first? #t))
  (let ((toclist (toc-list-filter 
		  (node-list-filter-by-gi (children nd)
					  (append (division-element-list)
						  (component-element-list)
						  (section-element-list)))))
	(wrappergi (if first? "chapters" "sub"))
	(wrapperattr (if first? '()  
(list
				 (list "name" (element-title-string nd))
				 (list "link" (href-to nd)))
)))
    (if (or (<= depth 0) 
	    (and (node-list-empty? toclist) #f))
	(empty-sosofo)
	(make element gi: wrappergi
	      attributes: wrapperattr
		    (let loop ((nl toclist))
		      (if (node-list-empty? nl)
			  (empty-sosofo)
			  (sosofo-append
			    (build-devhelp-toc (node-list-first nl) 
				       (- depth 1) #f)
			    (loop (node-list-rest nl)))))))))


(define (make-devhelp-chapters) 
  (build-devhelp-toc (sgml-root-element) (devhelp-toc-depth)))

;; Index processing (based on dbindes.dsl, v1.76)

(define (devhelpindexattr attr)
  (if (attribute-string (normalize attr))
      (make sequence
	(make formatting-instruction data: attr)
	(make formatting-instruction data: " ")
	(make formatting-instruction data: (attribute-string 
					    (normalize attr)))
	(htmlnewline))
      (empty-sosofo)))

(define (devhelpindexterm)
  (let* ((attr    (gi (current-node)))
	 (content (data (current-node)))
	 (string  (string-replace content "&#13;" " "))
	 (sortas  (attribute-string (normalize "sortas"))))
    (make sequence
      (make formatting-instruction data: string))))

(define (devhelpindexzone zone)
  (let loop ((idlist (split zone)))
    (if (null? idlist)
	(empty-sosofo)
	(make sequence
	  (devhelpindexzone1 (car idlist))
	  (loop (cdr idlist))))))

(define (devhelpindexzone1 id)
  (let* ((target (ancestor-member (element-with-id id)
				  (append (book-element-list)
					  (division-element-list)
					  (component-element-list)
					  (section-element-list))))
	 (title  (string-replace (element-title-string target) "&#13;" " ")))
    (make sequence
      (make formatting-instruction data: "ZONE ")
      (make formatting-instruction data: (href-to target))
      (htmlnewline)

      (make formatting-instruction data: "TITLE ")
      (make formatting-instruction data: title)
      (htmlnewline))))

(mode devhelpindex
  ;; this mode is really just a hack to get at the root element
  (root (process-children))

  (default 
    (if (node-list=? (current-node) (sgml-root-element))
	  (process-node-list (select-elements 
			      (descendants (current-node))
			      (normalize "indexterm")))
	(empty-sosofo)))

  (element indexterm
      (make sequence
	(make formatting-instruction data: "\less-than-sign;function")

	(make formatting-instruction data: " name=\"")

;;	(devhelpindexattr "scope")
;;	(devhelpindexattr "significance")
;;	(devhelpindexattr "class")
;;	(devhelpindexattr "id")
;;	(devhelpindexattr "startref")
	
;;	(if (attribute-string (normalize "zone"))
;;	    (devhelpindexzone (attribute-string (normalize "zone")))
;;	    (empty-sosofo))

	(process-children)

	(make formatting-instruction data: "\"")

	(make formatting-instruction data: (string-append " link=\"" (href-to (current-node)) "\""))

	(make formatting-instruction data: "/\greater-than-sign;&#13;")))
		    
  (element primary
    (devhelpindexterm))

;;  (element secondary
;;    (devhelpindexterm))

;;  (element tertiary
;;    (devhelpindexterm))

;;  (element see
;;    (devhelpindexterm))

;;  (element seealso
;;    (devhelpindexterm))
)

(define (make-devhelp-functions) 
  (make element gi: "functions"
	(with-mode devhelpindex
	 (process-children))))

;; Generates a devhelp spec

(define (make-devhelp)
  (make entity
    system-id: "book.devhelp"
    (make formatting-instruction data: "\less-than-sign;?xml version=\"1.0\"?\greater-than-sign;&#13;")
    (make element gi: "book"
	    attributes: (list 
		(list "name" %devhelp-name%)
		(list "version" %devhelp-version%)
		(list "title" (element-title-string (sgml-root-element)))
		(list "link" (html-base-filename (sgml-root-element))))
	  (make-devhelp-chapters)
          (make-devhelp-functions))))

;; Overrides the root node definition (taken from docbook.dsl, v1.76)

(root
 (make sequence
   (process-children)
   (with-mode manifest
     (process-children))
   (if html-index
       (with-mode htmlindex
	 (process-children))
       (empty-sosofo))
   (make-devhelp))
)

</style-specification-body>
</style-specification>

<external-specification id="docbook" document="dbstyle">

</style-sheet>
